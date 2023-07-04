from fastapi import HTTPException, status

does_not_exist = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Такой записи нет в базе!"
)

unique_error = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Такое имя уже занято"
)

data_error = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Целое число вне диапазона",
)
