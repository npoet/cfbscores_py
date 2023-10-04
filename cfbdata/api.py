from fastapi import APIRouter

from .data import get_final, get_team_info

router = APIRouter()


@router.get("/final")
def get_scores():
    return get_final()
