from fastapi import APIRouter, HTTPException
from pathlib import Path
import json

router = APIRouter()

def read_json_from_file(planet: str, case: int, data_type: str):
    # planet 조건 분기
    if planet not in ["Mars", "Earth"]:
        raise HTTPException(status_code=400, detail=f"Unknown planet: {planet}")

    # case 조건 분기
    if case not in range(1, 7):
        raise HTTPException(status_code=400, detail=f"Unknown case: {case}")

    # 동적으로 파일 이름 생성
    filename = f"{planet}_{case}.json"

    # getinfo.py 파일 기준으로 data 폴더까지의 상대 경로 설정
    base_dir = Path(__file__).resolve().parent.parent  # BE 폴더로 이동
    file_path = base_dir / "data" / data_type / filename

    # 경로 디버깅용 출력
    print(f"Attempting to read file from: {file_path.resolve()}")

    # 파일 존재 여부 확인
    if not file_path.exists():
        raise HTTPException(status_code=404, detail=f"File not found at {file_path.resolve()}")

    # 파일 읽기 시도
    try:
        with file_path.open("r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Failed to decode JSON")

# 기본 정보 엔드포인트
@router.get("/date")
async def get_info(planet: str, case: int):
    return read_json_from_file(planet, case, data_type="date")

# 바람 정보 엔드포인트
@router.get("/wind")
async def get_wind(planet: str, case: int):
    return read_json_from_file(planet, case, data_type="wind")

# 압력 정보 엔드포인트
@router.get("/pressure")
async def get_pressure(planet: str, case: int):
    return read_json_from_file(planet, case, data_type="pressure")

# 스펙토그램 정보 엔드포인트
@router.get("/spectrogram")
async def get_seismic(planet: str, case: int):
    return read_json_from_file(planet, case, data_type="spectrogram")

# 순수 지진 정보 엔드포인트
@router.get("/seismic")
async def get_seismic(planet: str, case: int):
    return read_json_from_file(planet, case, data_type="seismic")

# 노이즈 정보 엔드포인트
@router.get("/noise")
async def get_seismic(planet: str, case: int):
    return read_json_from_file(planet, case, data_type="noise")
