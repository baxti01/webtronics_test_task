# Webtronics test task
### Стек технологий
- FastApi
- JWT Auth
- SQLAlchemy
- Pydantic
- PostgreSQL
- Alembic
- Docker
- Uvicorn

---
## Запуск проекта
#### Создаём .env файл и добавляем следующие настройки

- Настройки сервера
  - `SERVER_HOST=`... (поумолчанию 0.0.0.0)
  - `SERVER_PORT=`... (поумолчанию 8000)
- Настройки базы данных 
  - `POSTGRES_HOST=`... (поумолчанию 0.0.0.0) установить как (db) для docker
  - `POSTGRES_PORT=`... (поумолчанию 5432)
  - `POSTGRES_DB=`... (обязательное поле)
  - `POSTGRES_USER=`... (обязательное поле)
  - `POSTGRES_PASSWORD=`... (обязательное поле)
- Настройки JWT Auth
  - `JWT_SECRET=`... (обязательное поле)
  - `JWT_ALGORITHM=`... (обязательное поле)
  - `JWT_ACCESS_TOKEN_EXPIRE=`... (обязательное поле)
  - `JWT_REFRESH_TOKEN_EXPIRE=`... (обязательное поле)

#### Запускаем проект на компьютере
Устанавливаем зависимости.
```
pip install -r requirements.txt
```

И старт проекта.
```
python main.py
```

#### Запускаем проект в docker. 
Но для этого обязательно укажите **POSTGRES_HOST=db**

```
docker-compose up
```

И пользуемся!

---