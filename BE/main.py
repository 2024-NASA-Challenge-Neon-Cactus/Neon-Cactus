from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from router import getinfo  # 필요한 모든 라우터들을 가져옵니다.

# FastAPI 애플리케이션 초기화
app = FastAPI()
router = APIRouter()

# CORS 설정 추가
origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 리스트
    allow_credentials=True,  # 쿠키를 포함한 자격 증명 허용 여부
    allow_methods=["*"],  # 허용할 HTTP 메서드 (GET, POST 등) - "*"로 모든 메서드 허용
    allow_headers=["*"],  # 허용할 HTTP 헤더 - "*"로 모든 헤더 허용
)

# 라우터 등록
app.include_router(getinfo.router, prefix="/getinfo")

# 기본 경로
@app.get("/")
async def read_root():
    return {"message": "Welcome to FastAPI project"}

