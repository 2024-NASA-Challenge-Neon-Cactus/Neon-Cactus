import os
import pandas as pd

# 데이터를 처리할 디렉토리 목록
directories = ['./date', './pressure', './seismic', './wind']
output_dir = './merged'  # 파일을 합친 결과를 저장할 디렉토리

# 결과를 저장할 디렉토리 생성
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 각 디렉토리의 파일들을 불러오고 같은 이름의 파일을 찾아 합치기
def merge_files_with_same_name():
    file_dict = {}

    # 각 디렉토리의 파일명을 정리
    for directory in directories:
        for filename in os.listdir(directory):
            if filename.endswith('.json'):  # json 파일만 처리
                filepath = os.path.join(directory, filename)
                if filename not in file_dict:
                    file_dict[filename] = []
                file_dict[filename].append(filepath)

    # 같은 이름의 파일을 하나로 합침
    for filename, filepaths in file_dict.items():
        merged_data = []

        # 각 파일에서 데이터를 읽어들임
        for filepath in filepaths:
            data = pd.read_json(filepath)  # json 파일 읽기
            merged_data.append(data)

        # 데이터들을 하나로 합침
        combined_data = pd.concat(merged_data, ignore_index=True)

        # 3000개씩 잘라서 저장
        for i in range(0, len(combined_data), 3000):
            chunk = combined_data.iloc[i:i+3000]
            chunk_filename = f"{filename}_part_{i//3000 + 1}.csv"
            chunk_filepath = os.path.join(output_dir, chunk_filename)
            chunk.to_csv(chunk_filepath, index=False)
            print(f"Saved {chunk_filename}")

merge_files_with_same_name()
