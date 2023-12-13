from espn.utils import convert_time


def create_base_obj_basketball(input_list, game_type):
    """
    create_base_obj_basketball converts raw json data to a basketball scheduled/live game dict from inputs and returns a list
    :param input_list: raw ESPN json response from func like basketball.get_cbb()
    :param game_type: Competition level in ["CBB"]
    :return: [{game1}, ... {gameN}] sorted by date ascending
    """
    scores = []
    for i in input_list:
        if i["status"]["type"]["state"] == "pre":
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
                "time": convert_time(i["status"]["type"]["shortDetail"]),
                "date": i["date"],
                "type": game_type
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = "Off Air"
            try:
                obj["odds"] = f"{game_type} | " + i["competitions"][0]["odds"][0]["details"]
            except KeyError:
                obj["odds"] = game_type
            try:
                rank = i["competitions"][0]["competitors"][1]["curatedRank"]["current"]
                if rank <= 25:
                    obj["away"] = "#" + str(rank) + " " + obj["away"]
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
                "type": game_type
            }
            try:
                obj["tv"] = i["competitions"][0]["geoBroadcasts"][0]["media"]["shortName"]
            except IndexError:
                obj["tv"] = f"{game_type}"
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
    return scores
