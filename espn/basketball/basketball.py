import requests
from espn.basketball.data import create_base_obj_basketball


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
    return create_base_obj_basketball(res, "CBB")
