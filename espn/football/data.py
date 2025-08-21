import requests

from espn.football.football_base import FootballBaseObject


def get_fbs():
    """
    get_fbs creates and returns a list of football score/schedule dicts for Football Bowl Subdivision 1-A
    :return: Result of data.create_base_obj_football(): [{game1}, ... {gameN}] sorted by date ascending
    """
    url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    params = {
        "groups": 80,  # all FBS, remove for top 25
    }
    res = requests.get(url, params=params).json()["events"]
    return get_football_games(res, "FBS")


def get_fcs():
    """
    get_fcs creates and returns a list of football score/schedule dicts for Football Championship Subdivision 1-AA
    :return: Result of data.create_base_obj_football(): [{game1}, ... {gameN}] sorted by date ascending
    """
    url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    params = {
        "groups": 81,  # all FCS
    }
    res = requests.get(url, params=params).json()["events"]
    return get_football_games(res, "FCS")


def get_nfl():
    """
    get_nfl creates and returns a list of football score/schedule dicts for the National Football League
    :return: Result of data.create_base_obj_football(): [{game1}, ... {gameN}] sorted by date ascending
    """
    url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    res = requests.get(url).json()["events"]
    return get_football_games(res, "NFL")


def get_football_games(input_list, game_type):
    """Convert ESPN football JSON to standardized list of dicts."""
    results = []
    for raw in input_list:
        try:
            obj = FootballBaseObject(raw, game_type)
            if obj.obj:  # skip empty (like TBD games)
                results.append(obj.to_dict())
        except:
            continue
    return results
