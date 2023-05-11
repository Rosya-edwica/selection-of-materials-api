from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

NOT_FOUND = JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=jsonable_encoder({"message": "Не удалось ничего вернуть"})
    )

