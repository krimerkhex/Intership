from fastapi import HTTPException, APIRouter

calc_route = APIRouter(prefix="/calc", tags=["calculator"])


@calc_route.get("/sum")
def sum_numbers(a: float, b: float):
    return {"result": a + b}


@calc_route.get("/multiply")
async def multiply_numbers(a: float, b: float):
    return {"result": a * b}


@calc_route.get("/divide")
async def divide_numbers(a: float, b: float):
    if b == 0:
        raise HTTPException(status_code=400, detail="Zero division error")
    return {"result": a / b}
