from espn.utils import convert_time
from espn.sports import SportsBaseObject


class SoccerBaseObject(SportsBaseObject):
    def _build_pre_game(self):
        if "TBD" in self.raw.get("shortName", "") or "TBA" in self.raw.get(
            "shortName", ""
        ):
            return
        home, away, comps = self._base_team_info()
        self.obj.update(
            {
                "home_id": home["team"]["location"],
                "home": home["team"]["abbreviation"],
                "home_site": home["team"]["links"][0]["href"],
                "home_mascot": home.get("form", ""),
                "away_id": away["team"]["location"],
                "away": away["team"]["abbreviation"],
                "away_site": away["team"]["links"][0]["href"],
                "away_mascot": away.get("form", ""),
                "time": convert_time(comps["startDate"]),
                "date": self.raw["date"],
                "type": self.game_type,
            }
        )
        self._add_common_fields(home, away, comps)
        self._add_odds(comps, index=1)
        self._add_leaders(home, away)

    def _build_in_game(self):
        home, away, comps = self._base_team_info()
        self.obj.update(
            {
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
        )
        self._add_common_fields(home, away, comps)

    def _build_post_game(self):
        home, away, comps = self._base_team_info()
        self.obj.update(
            {
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
        )
        self._add_common_fields(home, away, comps)
        self._add_headline(comps)

    def _add_leaders(self, home, away):
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
