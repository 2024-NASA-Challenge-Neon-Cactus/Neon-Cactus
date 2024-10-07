from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import json
import os
from pathlib import Path

router = APIRouter()

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
    
    # getinfo.py 파일 기준으로 data 폴더까지의 상대 경로 설정
    base_dir = Path(__file__).resolve().parent.parent  # BE 폴더로 이동
    file_path = base_dir / "data" / filename

    # 경로 디버깅용 출력
    print(f"Attempting to read file from: {file_path.resolve()}")

    # 파일 존재 여부 확인
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found at {file_path.resolve()}")

    # 파일 읽기 시도
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode JSON")
    
