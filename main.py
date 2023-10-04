from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from espn.api import router as espn_router
from cfbdata.api import router as cfbd_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(espn_router)
app.include_router(cfbd_router)
