from fastapi import APIRouter
from .teams_service import TeamsService, get_team_season
import time

router = APIRouter()
service = TeamsService()
CACHE = {}
CACHE_TTL = 60 * 60  # 1 hour in seconds


def get_cached(team_id: str, endpoint: str, fetch_func):
    key = f"{endpoint}:{team_id.lower()}"
    now = time.time()
    if key in CACHE and now - CACHE[key]["timestamp"] < CACHE_TTL:
        return CACHE[key]["data"]
    data = fetch_func(team_id)
    CACHE[key] = {"data": data, "timestamp": now}
    return data


@router.get("/team/{team_id}")
def get_team(team_id: str):
    return get_cached(team_id, "team", service.get_team_info)


@router.get("/season/{team_id}")
def get_season(team_id: str):
    return get_cached(team_id, "season", lambda t: get_team_season(t))


@router.get("/record/{team_id}")
def get_record(team_id: str):
    return get_cached(team_id, "record", service.get_team_records)
