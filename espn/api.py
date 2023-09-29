from fastapi import APIRouter

from .data import get_cfb, get_nfl

router = APIRouter()


@router.get("/scores")
def get_scores():
    all_scores = get_cfb() + get_nfl()
    return sorted(all_scores, key=lambda k: k['date'])
