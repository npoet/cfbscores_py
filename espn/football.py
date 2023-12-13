import requests
from .data import create_base_obj_football


def get_cfb():
    url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    params = {
        "groups": 80,  # all FBS, remove for top 25
    }
    res = requests.get(url, params=params).json()["events"]
    scores = create_base_obj_football(res, "FBS")
    return scores


def get_fcs():
    url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    params = {
        "groups": 81,  # all FCS
    }
    res = requests.get(url, params=params).json()["events"]
    scores = create_base_obj_football(res, "FCS")
    return scores


def get_nfl():
    url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    res = requests.get(url).json()["events"]
    scores = create_base_obj_football(res, "NFL")
    return scores
