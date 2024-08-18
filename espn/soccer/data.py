from espn.utils import convert_time


def create_base_obj_soccer(input_list, game_type):
    """
    create_base_obj_soccer creates and returns a list of soccer score/schedule dicts
    :param input_list: raw ESPN json response from func like soccer.get_schedule()
    :param game_type: Competition level in ["MLS", "INTL", "EPL", "UEFA"]
    :return: [{game1}, ... {gameN}] sorted by date ascending
    """
    scores = []
    for i in input_list:
        if i["status"]["type"]["state"] == "pre" and "TBD" not in i["shortName"] and "TBA" not in i["shortName"]:
            obj = {
                "home_id": i["competitions"][0]["competitors"][0]["team"]["location"],
                "home": i["competitions"][0]["competitors"][0]["team"]["abbreviation"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away_id": i["competitions"][0]["competitors"][1]["team"]["location"],
                "away": i["competitions"][0]["competitors"][1]["team"]["abbreviation"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "time": convert_time(i["status"]["type"]["shortDetail"]),
                "date": i["date"],
                "type": game_type
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = "Off Air"
            scores.append(obj)
        elif i["status"]["type"]["state"] == "post":
            obj = {
                "home_id": i["competitions"][0]["competitors"][0]["team"]["location"],
                "home": i["competitions"][0]["competitors"][0]["team"]["abbreviation"],
                "home_site": i["competitions"][0]["competitors"][0]["team"]["links"][0]["href"],
                "home_record": i["competitions"][0]["competitors"][0]["records"][0]["summary"],
                "home_logo": i["competitions"][0]["competitors"][0]["team"]["logo"],
                "away_id": i["competitions"][0]["competitors"][1]["team"]["location"],
                "away": i["competitions"][0]["competitors"][1]["team"]["abbreviation"],
                "away_site": i["competitions"][0]["competitors"][1]["team"]["links"][0]["href"],
                "away_record": i["competitions"][0]["competitors"][1]["records"][0]["summary"],
                "away_logo": i["competitions"][0]["competitors"][1]["team"]["logo"],
                "home_score": i["competitions"][0]["competitors"][0]["score"],
                "away_score": i["competitions"][0]["competitors"][1]["score"],
                "date": i["date"],
                "type": game_type
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = "Off Air"
            scores.append(obj)
    return scores
