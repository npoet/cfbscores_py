import requests


def get_cfb():
    url = "http://site.api.espn.com/apis/site/v2/sports/football/college-football/scoreboard"
    params = {
        "groups": 80,  # all FBS, remove for top 25
    }
    res = requests.get(url, params=params).json()["events"]
    scores = []
    for i in res:
        if i["status"]["type"]["state"] == "pre":
            obj = {
                "home": i["competitions"][0]["competitors"][0]["team"]["abbreviation"],
                "home_conf": i["competitions"][0]["competitors"][0]["records"][3]["summary"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["abbreviation"],
                "away_conf": i["competitions"][0]["competitors"][1]["records"][3]["summary"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "time": i["status"]["type"]["shortDetail"],
                "date": i["date"],
                "type": "College"
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
            try:
                home_pas = i["competitions"][0]["competitors"][0]["leaders"][0]["leaders"][0]
                home_rush = i["competitions"][0]["competitors"][0]["leaders"][1]["leaders"][0]
                home_rec = i["competitions"][0]["competitors"][0]["leaders"][2]["leaders"][0]
                obj["home_pass"] = (
                        home_pas["athlete"]["position"]["abbreviation"] +
                        home_pas["athlete"]["jersey"] + " " +
                        home_pas["displayValue"]
                )
                obj["home_rush"] = (
                        home_rush["athlete"]["position"]["abbreviation"] +
                        home_rush["athlete"]["jersey"] + " " +
                        home_rush["displayValue"]
                )
                obj["home_rec"] = (
                        home_rec["athlete"]["position"]["abbreviation"] +
                        home_rec["athlete"]["jersey"] + " " +
                        home_rec["displayValue"]
                )
            except KeyError:
                pass
            try:
                away_pas = i["competitions"][0]["competitors"][1]["leaders"][0]["leaders"][0]
                away_rush = i["competitions"][0]["competitors"][1]["leaders"][1]["leaders"][0]
                away_rec = i["competitions"][0]["competitors"][1]["leaders"][2]["leaders"][0]
                obj["away_pass"] = (
                        away_pas["athlete"]["position"]["abbreviation"] +
                        away_pas["athlete"]["jersey"] + " " +
                        away_pas["displayValue"]
                )
                obj["away_rush"] = (
                        away_rush["athlete"]["position"]["abbreviation"] +
                        away_rush["athlete"]["jersey"] + " " +
                        away_rush["displayValue"]
                )
                obj["away_rec"] = (
                        away_rec["athlete"]["position"]["abbreviation"] +
                        away_rec["athlete"]["jersey"] + " " +
                        away_rec["displayValue"]
                )
            except KeyError:
                pass
            scores.append(obj)
        elif i["status"]["type"]["state"] == "in":
            obj = {
                "home": i["competitions"][0]["competitors"][0]["team"]["abbreviation"],
                "home_conf": i["competitions"][0]["competitors"][0]["records"][3]["summary"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["abbreviation"],
                "away_conf": i["competitions"][0]["competitors"][1]["records"][3]["summary"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "home_score": i["competitions"][0]["competitors"][0]["score"],
                "away_score": i["competitions"][0]["competitors"][1]["score"],
                "time": i["status"]["type"]["shortDetail"],
                "date": i["date"],
                "type": "College"
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
            try:
                pass_leader = i["competitions"][0]["leaders"][0]["leaders"][0]
                rush_leader = i["competitions"][0]["leaders"][1]["leaders"][0]
                rec_leader = i["competitions"][0]["leaders"][2]["leaders"][0]
                obj["pass_leader"] = (
                        pass_leader["athlete"]["position"]["abbreviation"] +
                        pass_leader["athlete"]["jersey"] + " " +
                        pass_leader["athlete"]["shortName"] + " " +
                        pass_leader["displayValue"]
                )
                obj["rush_leader"] = (
                        rush_leader["athlete"]["position"]["abbreviation"] +
                        rush_leader["athlete"]["jersey"] + " " +
                        rush_leader["athlete"]["shortName"] + " " +
                        rush_leader["displayValue"]
                )
                obj["rec_leader"] = (
                        rec_leader["athlete"]["position"]["abbreviation"] +
                        rec_leader["athlete"]["jersey"] + " " +
                        rec_leader["athlete"]["shortName"] + " " +
                        rec_leader["displayValue"]
                )
            except KeyError:
                pass
            try:
                obj["last_play"] = i["competitions"][0]["situation"]["lastPlay"]["text"]
            except KeyError:
                pass
            try:
                prob = i["competitions"][0]["situation"]["lastPlay"]["probability"]
                home_prob = prob["homeWinPercentage"]
                away_prob = prob["awayWinPercentage"]
                max_prob = max(home_prob, away_prob)
                if max_prob == home_prob:
                    obj["win_prob"] = obj["home"] + str(home_prob) + "%"
                else:
                    obj["win_prob"] = obj["away"] + str(away_prob) + "%"
            except KeyError:
                pass
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
                "date": i["date"],
                "type": "NFL"
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
                rank = i["competitions"][0]["competitors"][1]["curatedRank"]["current"]
                if rank <= 25:
                    obj["away"] = "#" + str(rank) + " " + obj["away"]
            except KeyError:
                pass
            try:
                home_pas = i["competitions"][0]["competitors"][0]["leaders"][0]["leaders"][0]
                home_rush = i["competitions"][0]["competitors"][0]["leaders"][1]["leaders"][0]
                home_rec = i["competitions"][0]["competitors"][0]["leaders"][2]["leaders"][0]
                obj["home_pass"] = (
                        home_pas["athlete"]["position"]["abbreviation"] +
                        home_pas["athlete"]["jersey"] + " " +
                        home_pas["displayValue"]
                )
                obj["home_rush"] = (
                        home_rush["athlete"]["position"]["abbreviation"] +
                        home_rush["athlete"]["jersey"] + " " +
                        home_rush["displayValue"]
                )
                obj["home_rec"] = (
                        home_rec["athlete"]["position"]["abbreviation"] +
                        home_rec["athlete"]["jersey"] + " " +
                        home_rec["displayValue"]
                )
            except KeyError:
                pass
            try:
                away_pas = i["competitions"][0]["competitors"][1]["leaders"][0]["leaders"][0]
                away_rush = i["competitions"][0]["competitors"][1]["leaders"][1]["leaders"][0]
                away_rec = i["competitions"][0]["competitors"][1]["leaders"][2]["leaders"][0]
                obj["away_pass"] = (
                        away_pas["athlete"]["position"]["abbreviation"] +
                        away_pas["athlete"]["jersey"] + " " +
                        away_pas["displayValue"]
                )
                obj["away_rush"] = (
                        away_rush["athlete"]["position"]["abbreviation"] +
                        away_rush["athlete"]["jersey"] + " " +
                        away_rush["displayValue"]
                )
                obj["away_rec"] = (
                        away_rec["athlete"]["position"]["abbreviation"] +
                        away_rec["athlete"]["jersey"] + " " +
                        away_rec["displayValue"]
                )
            except KeyError:
                pass
            scores.append(obj)
        elif i["status"]["type"]["state"] == "in":
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
                "date": i["date"],
                "type": "NFL"
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
            try:
                pass_leader = i["competitions"][0]["leaders"][0]["leaders"][0]
                rush_leader = i["competitions"][0]["leaders"][1]["leaders"][0]
                rec_leader = i["competitions"][0]["leaders"][2]["leaders"][0]
                obj["pass_leader"] = (
                        pass_leader["athlete"]["position"]["abbreviation"] +
                        pass_leader["athlete"]["jersey"] + " " +
                        pass_leader["athlete"]["shortName"] + " " +
                        pass_leader["displayValue"]
                )
                obj["rush_leader"] = (
                        rush_leader["athlete"]["position"]["abbreviation"] +
                        rush_leader["athlete"]["jersey"] + " " +
                        rush_leader["athlete"]["shortName"] + " " +
                        rush_leader["displayValue"]
                )
                obj["rec_leader"] = (
                        rec_leader["athlete"]["position"]["abbreviation"] +
                        rec_leader["athlete"]["jersey"] + " " +
                        rec_leader["athlete"]["shortName"] + " " +
                        rec_leader["displayValue"]
                )
            except KeyError:
                pass
            try:
                obj["last_play"] = i["competitions"][0]["situation"]["lastPlay"]["text"]
            except KeyError:
                pass
            try:
                prob = i["competitions"][0]["situation"]["lastPlay"]["probability"]
                home_prob = prob["homeWinPercentage"]
                away_prob = prob["awayWinPercentage"]
                max_prob = max(home_prob, away_prob)
                if max_prob == home_prob:
                    obj["win_prob"] = obj["home"] + " " + str(round(home_prob*100, 2)) + "%"
                else:
                    obj["win_prob"] = obj["away"] + " " + str(round(away_prob*100, 2)) + "%"
            except KeyError:
                pass
            scores.append(obj)
    return scores
