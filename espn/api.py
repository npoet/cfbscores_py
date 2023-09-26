from fastapi import APIRouter
import requests

router = APIRouter()


@router.get("/scores")
def get_scores():
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
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["location"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "time": i["status"]["type"]["shortDetail"],
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = ""
            try:
                obj["odds"] = i["competitions"][0]["odds"][0]["details"]
            except KeyError:
                obj["odds"] = ""
            scores.append(obj)
        else:
            obj = {
                "home": i["competitions"][0]["competitors"][0]["team"]["location"],
                "home_mascot": i["competitions"][0]["competitors"][0]["team"]["name"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away": i["competitions"][0]["competitors"][1]["team"]["location"],
                "away_mascot": i["competitions"][0]["competitors"][1]["team"]["name"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "home_score": i["competitions"][0]["competitors"][0]["score"],
                "away_score": i["competitions"][0]["competitors"][1]["score"],
                "time": i["status"]["displayClock"],
                "quarter": i["status"]["period"],
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = ""
            scores.append(obj)
    return scores
