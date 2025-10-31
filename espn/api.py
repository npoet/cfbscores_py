from fastapi import APIRouter
import requests

from espn.sports.football import get_fbs, get_fcs, get_nfl
from espn.sports.basketball import get_cbb
from espn.sports.soccer import get_epl

router = APIRouter()


@router.get("/scores")
async def get_scores():
    """
    get_scores combines each of the data feeds for ScoreboardGrid frontend display
    :return: sorted([{gameA1}...{gameAN} + {gameB1}...{gameBN} ... + {gameN1} ... {gameNN}])
    """
    all_scores = []
    # track used cfb game_ids, so they aren't duplicated through lower divisions
    cfb_game_ids = set()
    try:
        fbs = get_fbs()
        for game in fbs:
            all_scores.append(game)
            cfb_game_ids.add(game["game_id"])
    except requests.exceptions.JSONDecodeError:
        pass
    try:
        fcs = get_fcs()
        for game in fcs:
            game_id = game["game_id"]
            if game_id not in cfb_game_ids:
                all_scores.append(game)
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

    # keep only games that have a 'date' field
    all_scores = [g for g in all_scores if "date" in g]

    # re-sort overall list
    return sorted(all_scores, key=lambda k: k["date"])


@router.get("/football")
def get_football():
    """
    get_football combines each of the data feeds for ScoreboardGrid frontend display
    :return: sorted([{gameA1}...{gameAN} + {gameB1}...{gameBN} ... + {gameN1} ... {gameNN}])
    """
    all_scores = []
    # track used cfb game_ids, so they aren't duplicated through lower divisions
    cfb_game_ids = set()
    try:
        fbs = get_fbs()
        for game in fbs:
            all_scores.append(game)
            cfb_game_ids.add(game["game_id"])
    except requests.exceptions.JSONDecodeError:
        pass
    try:
        fcs = get_fcs()
        for game in fcs:
            game_id = game["game_id"]
            if game_id not in cfb_game_ids:
                all_scores.append(game)
    except requests.exceptions.JSONDecodeError:
        pass
    try:
        all_scores += get_nfl()
    except requests.exceptions.JSONDecodeError:
        pass
    # re-sort overall list
    return sorted(all_scores, key=lambda k: k["date"])


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
    return sorted(all_scores, key=lambda k: k["date"])


@router.get("/soccer")
def get_soccer():
    """
    get_soccer combines each of the data feeds for ScoreboardGrid frontend display
    :return: sorted([{gameA1}...{gameAN} + {gameB1}...{gameBN} ... + {gameN1} ... {gameNN}])
    """
    all_scores = []
    try:
        all_scores += get_epl()
    except requests.exceptions.JSONDecodeError:
        pass
    return sorted(all_scores, key=lambda k: k["date"])
