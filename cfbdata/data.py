import requests


def get_current_week():
    url_espn = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    res = requests.get(url_espn).json()["week"]
    return res["number"]


def get_team_info(conf_id, team_id):
    url_cfbdata = "https://api.collegefootballdata.com"
    api_key = "FjnPRcXt2W7X2vYhNo0qbt+fKEu7WqVkz5+X73H8pqtJ9+T6Pe4huEOTnTLwBKkd"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "conference": conf_id,
    }
    res = requests.get(url_cfbdata + "/teams", headers=headers, params=params).json()
    for i in res:
        if i["id"] == team_id:
            return i


def calc_team_success_rate(team_id, week):
    # get current season, week
    # get plays by team_id for week, prev weeks
    # calc off. success rate: 1st Dn: 60%, 2nd Dn: 75%, 3rd Dn: 100% yards to go
    # calc def. success rate: 1st Dn: <=30%, 2nd Dn: <=50%, 3rd Dn: <=83% yards to go
    # net = successful / total plays
    # store prev weeks in db to minimize calcs
    pass


def get_final():
    url_cfbdata = "https://api.collegefootballdata.com"
    api_key = "FjnPRcXt2W7X2vYhNo0qbt+fKEu7WqVkz5+X73H8pqtJ9+T6Pe4huEOTnTLwBKkd"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {
        "year": 2023,
        "week": get_current_week(),
        "division": "fbs"
    }
    res = requests.get(url_cfbdata + "/games", headers=headers, params=params).json()
    games = []
    for i in res:
        if i["completed"]:
            home_info = get_team_info(i["home_conference"], i["home_id"])
            away_info = get_team_info(i["away_conference"], i["away_id"])
            obj = {
                "home": home_info["abbreviation"],
                "home_score": i["home_points"],
                "home_record": "",
                "home_logo": home_info["logos"][0],
                "away": away_info["abbreviation"],
                "away_score": i["away_points"],
                "away_record": "",
                "away_logo": away_info["logos"][0],
                "time": "Final"
            }
            games.append(obj)
    return games
