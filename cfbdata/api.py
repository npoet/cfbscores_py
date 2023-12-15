import os
from datetime import datetime

from fastapi import APIRouter

import cfbd

config = cfbd.Configuration()
config.api_key['Authorization'] = os.environ["CFBD_API_KEY"]
config.api_key_prefix['Authorization'] = 'Bearer'

ratings = cfbd.RatingsApi(cfbd.ApiClient(config))
games = cfbd.GamesApi(cfbd.ApiClient(config))
router = APIRouter()


@router.get("/team/{team_id}")
def get_team_info(team_id):
    """
    get_team_info builds team ratings page from cfbdata ratings/rankings statistics
    :param team_id: lowercase team name from input, can include spaces i.e. 'michigan', 'penn state'
    :return: json object containing sp+ ratings, elo rating, fpi, etc
    """
    resp_sp = ratings.get_sp_ratings(year=2023)
    team_ranking_sp = [r.ranking for r in resp_sp if r.team.lower() == team_id.lower()][0]
    resp_sp_team = ratings.get_sp_ratings(year=2023, team=team_id.lower())
    return_data = {}
    sp = resp_sp_team[0]
    return_data.update({
        "sp_ovr_ranking": team_ranking_sp,
        "sp_ovr_rating": sp.rating,
        "sp_off_rating": sp.offense.rating,
        "sp_def_rating": sp.defense.rating,
    })
    resp_elo = ratings.get_elo_ratings(year=2023, team=team_id.lower())
    return_data.update({
        "elo_ovr_rating": resp_elo[0].elo
    })
    resp_fpi = ratings.get_fpi_ratings(year=2023, team=team_id.lower())
    fpi = resp_fpi[0]
    return_data.update({
        "fpi_ovr_ranking": fpi.resume_ranks.fpi,
        "fpi_ovr_rating": fpi.fpi,
        "fpi_sos": fpi.resume_ranks.strength_of_schedule,
        "fpi_game_control": fpi.resume_ranks.game_control
    })
    return return_data


@router.get("/season/{team_id}")
def get_team_season(team_id):
    """
    get_team_season looks up games for the given team_id and current active season and returns a schedule list
    :param team_id: lowercase team name from input, can include spaces i.e. 'michigan', 'penn state'
    :return:
    """
    resp_games = games.get_games(year=2023, team=team_id)
    season = []
    for game in resp_games:
        obj = {
            "home": game.home_team,
            "away": game.away_team,
            "home_score": game.home_points,
            "away_score": game.away_points,
            "date": datetime.fromisoformat(game.start_date).date(),
        }
        if game.notes is not None:
            obj.update({"note": game.notes})
        season.append(obj)
    return season
