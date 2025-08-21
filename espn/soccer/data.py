import requests
from espn.soccer.soccer_base import SoccerBaseObject


def get_epl():
    """
    get_soccer creates and returns a list of soccer score/schedule dicts for various leagues
    :return: Result of data.create_base_obj_soccer(): [{game1}, ... {gameN}] sorted by date ascending
    """
    url = "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    res = requests.get(url).json()["events"]
    return get_soccer_games(res, "EPL")


def get_soccer_games(input_list, game_type):
    """Convert ESPN football JSON to standardized list of dicts."""
    results = []
    for raw in input_list:
        try:
            obj = SoccerBaseObject(raw, game_type)
            if obj.obj:  # skip empty (like TBD games)
                results.append(obj.to_dict())
        except:
            continue
    return results
