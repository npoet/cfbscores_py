import requests


def get_cfb():
    url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    params = {
        # "year": 2023
        "groups": 80,  # all FBS, remove for top 25
    }
    res = requests.get(url, params=params).json()["events"]
    scores = []
    for i in res:
        if i["status"]["type"]["state"] == "pre":
            obj = {
                "home": i["competitions"][0]["competitors"][0]["team"]["location"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["location"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "time": i["status"]["type"]["shortDetail"],
                "date": i["date"]
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = "Off Air"
            try:
                obj["odds"] = i["competitions"][0]["odds"][0]["details"]
            except KeyError:
                obj["odds"] = "No Line"
            try:
                rank = i["competitions"][0]["competitors"][0]["curatedRank"]["current"]
                if rank <= 25:
                    obj["home"] = "#" + str(rank) + " " + obj["home"]
            except KeyError:
                pass
            try:
                rank = i["competitions"][0]["competitors"][1]["curatedRank"]["current"]
                if rank <= 25:
                    obj["away"] = "#" + str(rank) + " " + obj["away"]
            except KeyError:
                pass
            scores.append(obj)
        else:
            obj = {
                "home": i["competitions"][0]["competitors"][0]["team"]["abbreviation"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["abbreviation"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "home_score": i["competitions"][0]["competitors"][0]["score"],
                "away_score": i["competitions"][0]["competitors"][1]["score"],
                "time": i["status"]["type"]["shortDetail"],
                "date": i["date"]
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = "Off Air"
            try:
                rank = i["competitions"][0]["competitors"][0]["curatedRank"]["current"]
                if rank <= 25:
                    obj["home"] = "#" + str(rank) + " " + obj["home"]
            except KeyError:
                pass
            try:
                rank = i["competitions"][0]["competitors"][1]["curatedRank"]["current"]
                if rank <= 25:
                    obj["away"] = "#" + str(rank) + " " + obj["away"]
            except KeyError:
                pass
            try:
                home_id = i["competitions"][0]["competitors"][0]["id"]
                poss_id = i["competitions"][0]["situation"]["possession"]
                ball_on = i["competitions"][0]["situation"]["possessionText"]
                if poss_id == home_id:
                    obj["possession"] = "home"
                    obj["ball_on"] = ball_on
                else:
                    obj["possession"] = "away"
                    obj["ball_on"] = ball_on
            except KeyError:
                obj["possession"] = ""
                obj["ball_on"] = ""
            scores.append(obj)
    return scores


def get_nfl():
    url = "http://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"
    res = requests.get(url).json()["events"]
    scores = []
    for i in res:
        if i["status"]["type"]["state"] == "pre":
            obj = {
                "home": i["competitions"][0]["competitors"][0]["team"]["location"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["location"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "time": i["status"]["type"]["shortDetail"],
                "date": i["date"]
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = "Off Air"
            try:
                obj["odds"] = i["competitions"][0]["odds"][0]["details"]
            except KeyError:
                obj["odds"] = "No Line"
            try:
                rank = i["competitions"][0]["competitors"][0]["curatedRank"]["current"]
                if rank <= 25:
                    obj["home"] = "#" + str(rank) + " " + obj["home"]
            except KeyError:
                pass
            try:
                rank = i["competitions"][0]["competitors"][1]["curatedRank"]["current"]
                if rank <= 25:
                    obj["away"] = "#" + str(rank) + " " + obj["away"]
            except KeyError:
                pass
            scores.append(obj)
        else:
            obj = {
                "home": i["competitions"][0]["competitors"][0]["team"]["abbreviation"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["abbreviation"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "home_score": i["competitions"][0]["competitors"][0]["score"],
                "away_score": i["competitions"][0]["competitors"][1]["score"],
                "time": i["status"]["type"]["shortDetail"],
                "date": i["date"]
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = "Off Air"
            try:
                rank = i["competitions"][0]["competitors"][0]["curatedRank"]["current"]
                if rank <= 25:
                    obj["home"] = "#" + str(rank) + " " + obj["home"]
            except KeyError:
                pass
            try:
                rank = i["competitions"][0]["competitors"][1]["curatedRank"]["current"]
                if rank <= 25:
                    obj["away"] = "#" + str(rank) + " " + obj["away"]
            except KeyError:
                pass
            try:
                home_id = i["competitions"][0]["competitors"][0]["id"]
                poss_id = i["competitions"][0]["situation"]["possession"]
                ball_on = i["competitions"][0]["situation"]["possessionText"]
                if poss_id == home_id:
                    obj["possession"] = "home"
                    obj["ball_on"] = ball_on
                else:
                    obj["possession"] = "away"
                    obj["ball_on"] = ball_on
            except KeyError:
                obj["possession"] = ""
                obj["ball_on"] = ""
            scores.append(obj)
    return scores
