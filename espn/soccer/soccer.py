import requests
from espn.soccer.data import create_base_obj_soccer


def get_epl():
    """
    get_soccer creates and returns a list of soccer score/schedule dicts for various leagues
    :return: Result of data.create_base_obj_soccer(): [{game1}, ... {gameN}] sorted by date ascending
    """
    url = "http://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard"
    res = requests.get(url).json()["events"]
    # print(res)
    return create_base_obj_soccer(res, "EPL")
