import requests
from espn.sports.basketball.basketball_base import BasketballBaseObject


def get_cbb():
    """
    get_cbb creates and returns a list of basketball score/schedule dicts for NCAA Division 1
    :return: Result of data.create_base_obj_basketball(): [{game1}, ... {gameN}] sorted by date ascending
    """
    url = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"
    params = {
        "seasonType": 2,
        "group": 50,  # all D1A, remove for top 25
    }
    res = requests.get(url, params=params).json()["events"]
    return get_basketball_games(res, "CBB")


def get_basketball_games(input_list, game_type):
    """Convert ESPN basketball JSON to standardized list of dicts."""
    results = []
    for raw in input_list:
        try:
            obj = BasketballBaseObject(raw, game_type)
            if obj.obj:  # skip empty (like TBD games)
                results.append(obj.to_dict())
        except:
            continue
    return results
