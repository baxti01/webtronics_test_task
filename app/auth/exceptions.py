from fastapi import HTTPException, status

incorrect_data = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect username or password',
    headers={'WWW-Authenticate': 'Bearer'},
)

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Could not validate credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)

invalid_grant_type = HTTPException(
    detail="grant_type указан не верно",
    status_code=status.HTTP_400_BAD_REQUEST
)

deleted_user = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Пользователь с таким именем удалён из базы данных",
    headers={'WWW-Authenticate': 'Bearer'},
)
