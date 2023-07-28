from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from api.routes.controller import router


app = FastAPI(
    version="1.1",
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(exc: RequestValidationError):
    errors = exc.errors()
    match errors[0]["type"]:
        case "value_error.any_str.min_length": message = "Слишком короткий запрос"
        case "value_error.number.not_le": message = "Слишком большое число"
        case "value_error.number.not_gt": message = "Слишком маленькое число"
        case "value_error.missing": message = "Обязательное поле пропущено"
        case _: message = errors
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({
            "message": message, 
            "detail": errors, 
            "docs": "Ссылка на документацию: http://api.edwica.ru/docs"
            }),
    )

