import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import torch
import torch
import torch.nn as nn
import torchvision.transforms.functional as TF

# 크기가 맞지 않는 텐서를 자르는 방법 (torchvision.transforms.functional.center_crop 사용)
def crop_to_match(tensor, target_tensor):
    """
    tensor의 크기를 target_tensor의 크기에 맞게 자르는 함수
    """
    _, _, target_h, target_w = target_tensor.size()
    # torchvision.transforms.functional.center_crop을 사용하여 중심에서 자름
    tensor = TF.center_crop(tensor, (target_h, target_w))
    return tensor


def match_channels(tensor, target_channels):
    current_channels = tensor.size(1)
    if current_channels != target_channels:
        # GPU로 이동된 상태에서 Conv2d 생성 및 적용
        conv = nn.Conv2d(current_channels, target_channels, kernel_size=1).to(tensor.device)  # 장치 맞춤
        tensor = conv(tensor)
    return tensor

class UNet(nn.Module):
    def __init__(self, config):
        super(UNet, self).__init__()
        self.depths = config.depths
        self.filters_root = config.filters_root
        self.kernel_size = config.kernel_size
        self.dilation_rate = config.dilation_rate
        self.pool_size = config.pool_size
        self.n_channel = config.n_channel
        self.n_class = config.n_class
        self.drop_rate = config.drop_rate
        self.build_model()

    def conv_block(self, in_channels, out_channels, kernel_size, dilation_rate):
        return nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=(3,3), stride=(1,1), padding=(2,2), dilation=dilation_rate),
            nn.BatchNorm2d(out_channels),
            nn.ReLU(inplace=True),
            nn.Dropout2d(self.drop_rate)
        )

    def build_model(self):
        self.down_convs = nn.ModuleList()
        self.up_convs = nn.ModuleList()

        # Down-sampling path
        for i in range(self.depths):
            in_channels = self.n_channel if i == 0 else 2**(i-1) * self.filters_root
            out_channels = 2**i * self.filters_root
            self.down_convs.append(self.conv_block(in_channels, out_channels, self.kernel_size, self.dilation_rate))

        # Up-sampling path
        for i in range(self.depths - 2, -1, -1):
            in_channels = 2**i * self.filters_root
            out_channels = in_channels // 2
            self.up_convs.append(self.conv_block(in_channels * 2, out_channels, self.kernel_size, self.dilation_rate))

        # Output layer
        self.final_conv = nn.Conv2d(2 * self.filters_root, self.n_class, kernel_size=1)

    def forward(self, x):
        encodings = []

        # Down-sampling
        for i, down_conv in enumerate(self.down_convs):
            x = down_conv(x)
            # print('1 down : ', i, x.size())
            if i < self.depths - 1:
                encodings.append(x)
                x = nn.MaxPool2d(self.pool_size)(x)
                print('2 down : ', i, x.size())

        # Up-sampling
        for i, up_conv in enumerate(self.up_convs):
            x = nn.Upsample(scale_factor=self.pool_size, mode='bilinear', align_corners=True)(x)
            
            print('up : ', i, x.size())
            # 스킵 연결 시 크기 및 채널 수 맞추기
            encoding = encodings[-(i+1)]
            if encoding.size() != x.size():
                x = crop_to_match(x, encoding)  # 크기 맞추기
                x = match_channels(x, encoding.size(1))  # 채널 수 맞추기

            x = torch.cat([encoding, x], dim=1)
            x = up_conv(x)

        return self.final_conv(x)


# Configuration matching the TensorFlow version
class ModelConfig:
    batch_size = 20
    depths = 6
    filters_root = 8
    kernel_size = (3, 3)
    pool_size = (2, 2)
    dilation_rate = (1, 1)
    class_weights = [1.0, 1.0, 1.0]
    loss_type = "cross_entropy"
    weight_decay = 0.0
    optimizer = "adam"
    momentum = 0.9
    learning_rate = 0.01
    decay_step = 1e9
    decay_rate = 0.9
    drop_rate = 0.0
    X_shape = [31, 201, 2]
    Y_shape = [31, 201, 2]
    n_channel = X_shape[-1]
    n_class = Y_shape[-1]


# Instantiate the model and set the optimizer
config = ModelConfig()
model = UNet(config)

# Optimizer (Adam, matching the config)
optimizer = optim.Adam(model.parameters(), lr=config.learning_rate)

# Loss function (Cross-entropy loss with optional class weights)
class_weights = torch.tensor(config.class_weights, dtype=torch.float32)
criterion = nn.CrossEntropyLoss(weight=class_weights)


# Training step
def train_on_batch(X_batch, Y_batch, model, optimizer, criterion):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_batch)
    loss = criterion(outputs, Y_batch)
    loss.backward()
    optimizer.step()
    return loss.item()

