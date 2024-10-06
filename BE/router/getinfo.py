import json
from fastapi import APIRouter, HTTPException
from pathlib import Path
import math

router = APIRouter()

def clean_invalid_values(data):
    """NaN, Infinity, -Infinity 값을 None으로 변환"""
    if isinstance(data, dict):
        return {k: clean_invalid_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_invalid_values(item) for item in data]
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None
        return data
    return data

def limit_data_size(data, limit=3000):
    """리스트의 크기를 제한하는 함수"""
    if isinstance(data, list):
        print(f"원래 리스트 크기: {len(data)}")  # 디버깅: 원래 리스트 크기 출력
        limited_data = data[:limit]  # 리스트가 3,000개 이상이면 자르기
        print(f"제한된 리스트 크기: {len(limited_data)}")  # 디버깅: 제한된 리스트 크기 출력
        return limited_data
    return data

@router.get("/")
async def get_info(planet: str, case: int):
    response = {}

    # planet 조건 분기
    if planet == "Mars":
        response["planet"] = "Mars"
    elif planet == "Earth":
        response["planet"] = "Earth"
    else:
        raise HTTPException(status_code=400, detail=f"Unknown planet: {planet}")

    # case 조건 분기
    if case == 1:
        response["case"] = "1"
    elif case == 2:
        response["case"] = "2"
    elif case == 3:
        response["case"] = "3"
    elif case == 4:
        response["case"] = "4"
    elif case == 5:
        response["case"] = "5"
    elif case == 6:
        response["case"] = "6"
    else:
        raise HTTPException(status_code=400, detail=f"Unknown case: {case}")

    # 동적으로 파일 이름 생성
    filename = f"{planet}_{case}.json"

    # 폴더 경로 설정 (BE 폴더에서 data 폴더로 이동)
    base_dir = Path(__file__).resolve().parent.parent / "data"  # data 폴더로 이동
    directories = ["date", "pressure", "seismic", "wind"]  # 각 데이터를 저장한 폴더 목록

    combined_data = {}

    # 각 폴더에서 파일을 읽어와 병합
    for directory in directories:
        file_path = base_dir / directory / filename

        # 파일 존재 여부 확인
        if not file_path.exists():
            # 파일이 없을 때 "data not available" 처리
            combined_data[directory] = f"{directory} data not available"
            continue

        # 파일 읽기 시도
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

                # 파일 형식이 딕셔너리 또는 리스트 형식인지 확인
                if isinstance(data, dict):
                    cleaned_data = clean_invalid_values(data)  # NaN/Inf 처리
                    combined_data[directory] = cleaned_data  # 딕셔너리 값은 크기 제한하지 않음
                elif isinstance(data, list):
                    cleaned_data = clean_invalid_values(data)  # NaN/Inf 처리
                    limited_data = limit_data_size(cleaned_data)  # 최대 3,000개의 데이터로 자름
                    combined_data[directory] = limited_data
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Invalid JSON format in {directory}: expected dict or list, got {type(data).__name__}"
                    )
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Failed to decode JSON from {directory}")

    return combined_data
