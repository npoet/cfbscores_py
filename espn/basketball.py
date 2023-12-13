import requests
from .data import create_base_obj_basketball


def get_cbb():
    url = "http://site.api.espn.com/apis/site/v2/sports/basketball/mens-college-basketball/scoreboard"
    params = {
        "seasonType": 2,
        "group": 50,  # all D1A, remove for top 25
    }
    res = requests.get(url, params=params).json()["events"]
    scores = create_base_obj_basketball(res, "CBB")
    return scores
