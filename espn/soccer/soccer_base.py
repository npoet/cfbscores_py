from espn.utils import convert_time


class SoccerBaseObject:
    def __init__(self, raw_data: dict, game_type: str):
        self.raw = raw_data
        self.game_type = game_type
        self.obj = {}

        self.state = self.raw.get("status", {}).get("type", {}).get("state")

        if self.state == "pre":
            self._build_pre_game()
        elif self.state == "in":
            self._build_in_game()
        elif self.state == "post":
            self._build_post_game()

    def _base_team_info(self):
        comps = self.raw.get("competitions", [])[0]
        return comps["competitors"][0], comps["competitors"][1], comps

    def _build_pre_game(self):
        if "TBD" in self.raw.get("shortName", "") or "TBA" in self.raw.get("shortName", ""):
            return
        home, away, comps = self._base_team_info()
        self.obj = {
            "home_id": home["team"]["location"],
            "home": home["team"]["abbreviation"],
            "home_site": home["team"]["links"][0]["href"],
            "home_mascot": home.get("form", ""),  # recent form in mascot field
            "away_id": away["team"]["location"],
            "away": away["team"]["abbreviation"],
            "away_site": away["team"]["links"][0]["href"],
            "away_mascot": away.get("form", ""),
            "time": convert_time(comps["startDate"]),
            "date": self.raw["date"],
            "type": self.game_type,
        }
        self._add_common_fields(home, away, comps)
        self._add_odds(comps)
        self._add_leaders(home, away)

    def _build_in_game(self):
        home, away, comps = self._base_team_info()
        self.obj = {
            "home_id": home["team"]["location"],
            "home": home["team"]["abbreviation"],
            "home_site": home["team"]["links"][0]["href"],
            "home_mascot": home.get("form", ""),
            "away_id": away["team"]["location"],
            "away": away["team"]["abbreviation"],
            "away_site": away["team"]["links"][0]["href"],
            "away_mascot": away["team"]["name"],
            "home_score": home.get("score"),
            "away_score": away.get("score"),
            "time": self.raw["status"]["type"]["shortDetail"],
            "date": self.raw["date"],
            "type": self.game_type,
        }
        self._add_common_fields(home, away, comps)

    def _build_post_game(self):
        home, away, comps = self._base_team_info()
        self.obj = {
            "home_id": home["team"]["location"],
            "home": home["team"]["abbreviation"],
            "home_site": home["team"]["links"][0]["href"],
            "home_mascot": home.get("form", ""),
            "away_id": away["team"]["location"],
            "away": away["team"]["abbreviation"],
            "away_site": away["team"]["links"][0]["href"],
            "away_mascot": away["team"]["name"],
            "home_score": home.get("score"),
            "away_score": away.get("score"),
            "time": self.raw["status"]["type"]["shortDetail"],
            "date": self.raw["date"],
            "type": self.game_type,
        }
        self._add_common_fields(home, away, comps)
        self._add_headline(comps)

    def _add_common_fields(self, home, away, comps):
        self.obj["home_logo"] = home["team"].get("logo")
        self.obj["away_logo"] = away["team"].get("logo")
        self.obj["home_record"] = self._safe_get(home, ["records", 0, "summary"], "")
        self.obj["away_record"] = self._safe_get(away, ["records", 0, "summary"], "")
        try:
            tv = comps["geoBroadcasts"][0]["media"]["shortName"]
            self.obj["tv"] = tv if len(tv) <= 10 else "Off Air"
        except (KeyError, IndexError):
            self.obj["tv"] = "Off Air"

    def _add_odds(self, comps):
        try:
            self.obj["odds"] = f"{self.game_type} | " + comps["odds"][1]["details"]
        except (KeyError, IndexError):
            self.obj["odds"] = f"{self.game_type} | No Line"

    def _add_leaders(self, home, away):
        # for soccer, only passing leaders (goalscorers)
        for side, label in [(home, "home"), (away, "away")]:
            try:
                scorer = side["leaders"][0]["leaders"][0]
                self.obj[f"{label}_pass"] = (
                    f"{scorer['athlete']['position']['abbreviation']} "
                    f"{scorer['athlete']['jersey']} "
                    f"{scorer['athlete']['shortName']} "
                    f"{scorer['displayValue']} G"
                )
            except (KeyError, IndexError):
                pass

    def _add_headline(self, comps):
        try:
            self.obj["headline"] = comps["headlines"][0]["shortLinkText"]
        except (KeyError, IndexError):
            pass

    @staticmethod
    def _safe_get(d, path, default=None):
        try:
            for p in path:
                d = d[p]
            return d
        except KeyError:
            return default

    def to_dict(self):
        return self.obj
