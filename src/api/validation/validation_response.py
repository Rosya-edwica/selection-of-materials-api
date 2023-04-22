from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

BAD_REQUEST = JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"message": "2131"})
    )