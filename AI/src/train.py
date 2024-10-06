import os
import torch
from PIL import Image
from torchvision import transforms
import numpy as np
from UNet import UNet, ModelConfig


# 이미지 전처리 함수 (모델 입력 크기로 변환)
def preprocess_two_images(image_path1, image_path2, target_size=(31, 201)):
    # 두 이미지를 불러와 흑백(1채널)으로 변환
    image1 = Image.open(image_path1).convert('L')  # 첫 번째 이미지
    image2 = Image.open(image_path2).convert('L')  # 두 번째 이미지
    
    # 각 이미지를 동일하게 전처리 (크기 조정, 텐서 변환)
    transform = transforms.Compose([
        transforms.Resize(target_size),
        transforms.ToTensor()  # 텐서로 변환 (1채널, H, W)
    ])
    
    image1 = transform(image1)  # (1, H, W)
    image2 = transform(image2)  # (1, H, W)

    # 두 이미지를 결합하여 2채널로 만들기 (채널을 첫 번째 축으로 결합)
    combined_image = torch.cat([image1, image2], dim=0)  # (2, H, W)

    # 배치 차원 추가 (1, 2, H, W)
    combined_image = combined_image.unsqueeze(0)
    
    return combined_image
# 디렉터리 순회 후 UNet 모델로 예측값 반환 함수
def predict_from_directory(model, directory, device='cpu'):
    model.eval()  # 모델을 평가 모드로 설정 (dropout 등 비활성화)
    predictions = {}

    # 디렉터리 순회
    for filename in os.listdir(directory):
        if filename.endswith(".png") or filename.endswith(".jpg"):  # 이미지 파일만 선택
            image_path = os.path.join(directory, filename)
            print(f"Processing {image_path}...")

            # 이미지 전처리
            image_tensor = preprocess_two_images(image_path, image_path)

            # 모델 예측
            image_tensor = image_tensor.to(device)  # 장치로 이동 (GPU/CPU)
            with torch.no_grad():  # 예측할 때는 기울기 계산 비활성화
                output = model(image_tensor)

            # 예측값 처리
            prediction = torch.argmax(output, dim=1).cpu().numpy()  # (배치, 채널, H, W) -> (배치, H, W)
            predictions[filename] = prediction

    return predictions

# 예시 실행 코드
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# UNet 모델 정의 (이미 로드된 모델)
config = ModelConfig()
model = UNet(config)  # UNet 모델을 정의한 상태여야 함

# 모델을 GPU/CPU로 이동
model.to(device)

# 디렉터리 내 이미지 파일에 대해 예측 수행
directory = "../data/results/train"  # 이미지가 있는 디렉터리 경로
predictions = predict_from_directory(model, directory, device)

# 예측값 확인
for filename, pred in predictions.items():
    print(f"Prediction for {filename}: shape = {pred.shape}")
