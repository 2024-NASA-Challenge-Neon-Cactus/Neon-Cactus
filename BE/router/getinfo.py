from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/")
async def get_info(planet: str, event: str, case: int):
    response = {}

    # planet 조건 분기
    if planet == "mars":
        response["planet"] = "mars."
    elif planet == "earth":
        response["planet"] = "earth."
    else:
        raise HTTPException(status_code=400, detail=f"Unknown planet: {planet}")

    # event 조건 분기
    if event == "earthquakes":
        response["event"] = "earthquakes."
    elif event == "nonevent":
        response["event"] = "nonevent"
    else:
        raise HTTPException(status_code=400, detail=f"Unknown event: {event}")

    # case 조건 분기
    if case == 1:
        response["case"] = "1"
    elif case == 2:
        response["case"] = "2"
    elif case == 3:
        response["case"] = "3"
    else:
        raise HTTPException(status_code=400, detail=f"Unknown case: {case}")

    return response
