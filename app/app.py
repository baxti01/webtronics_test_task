from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import routers
from app.metadata import api_description, api_version, api_title, api_contacts, tags_metadata


app = FastAPI(
    title=api_title,
    version=api_version,
    description=api_description,
    contact=api_contacts,
    openapi_tags=tags_metadata
)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router)
