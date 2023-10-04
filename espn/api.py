from fastapi import APIRouter
import requests

from .data import get_cfb, get_nfl

router = APIRouter()


@router.get("/scores")
def get_scores():
    try:
        all_scores = get_cfb() + get_nfl()
    except requests.exceptions.JSONDecodeError:
        all_scores = get_cfb()

    return sorted(all_scores, key=lambda k: k['date'])
