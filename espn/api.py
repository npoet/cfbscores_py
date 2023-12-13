from fastapi import APIRouter
import requests

from .football import get_cfb, get_fcs, get_nfl
from .basketball import get_cbb

router = APIRouter()


@router.get("/scores")
def get_scores():
    all_scores = []
    try:
        all_scores += get_cfb()
    except requests.exceptions.JSONDecodeError:
        pass
    try:
        all_scores += get_fcs()
    except requests.exceptions.JSONDecodeError:
        pass
    try:
        all_scores += get_nfl()
    except requests.exceptions.JSONDecodeError:
        pass
    try:
        all_scores += get_cbb()
    except requests.exceptions.JSONDecodeError:
        pass
    return sorted(all_scores, key=lambda k: k['date'])
