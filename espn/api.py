from fastapi import APIRouter
import requests

from .football import get_fbs, get_fcs, get_nfl
from .basketball import get_cbb
from .soccer import get_epl

router = APIRouter()


@router.get("/scores")
async def get_scores():
    """
    get_scores combines each of the data feeds for ScoreboardGrid frontend display
    :return: sorted([{gameA1}...{gameAN} + {gameB1}...{gameBN} ... + {gameN1} ... {gameNN}])
    """
    all_scores = []
    try:
        all_scores += get_fbs()
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
        all_scores += get_epl()
    except requests.exceptions.JSONDecodeError:
        pass
    return sorted(all_scores, key=lambda k: k['date'])


@router.get("/football")
def get_football():
    """
    get_football combines each of the data feeds for ScoreboardGrid frontend display
    :return: sorted([{gameA1}...{gameAN} + {gameB1}...{gameBN} ... + {gameN1} ... {gameNN}])
    """
    all_scores = []
    try:
        all_scores += get_fbs()
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
    return sorted(all_scores, key=lambda k: k['date'])


@router.get("/basketball")
def get_basketball():
    """
    get_basketball combines each of the data feeds for ScoreboardGrid frontend display
    :return: sorted([{gameA1}...{gameAN} + {gameB1}...{gameBN} ... + {gameN1} ... {gameNN}])
    """
    all_scores = []
    try:
        all_scores += get_cbb()
    except requests.exceptions.JSONDecodeError:
        pass
    return all_scores


@router.get("/soccer")
def get_soccer():
    """
    get_soccer combines each of the data feeds for ScoreboardGrid frontend display
    :return: sorted([{gameA1}...{gameAN} + {gameB1}...{gameBN} ... + {gameN1} ... {gameNN}])
    """
    return get_epl()
