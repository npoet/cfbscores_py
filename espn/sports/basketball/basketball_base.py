from espn.utils import convert_time
from espn.sports import SportsBaseObject


class BasketballBaseObject(SportsBaseObject):
    def _build_pre_game(self):
        home, away, comps = self._base_team_info()
        self.obj.update(
            {
                "home": home["team"]["abbreviation"],
                "home_site": home["team"]["links"][0]["href"],
                "home_mascot": home["team"]["name"],
                "away": away["team"]["abbreviation"],
                "away_site": away["team"]["links"][0]["href"],
                "away_mascot": away["team"]["name"],
                "time": convert_time(self.raw["status"]["type"]["shortDetail"]),
                "date": self.raw["date"],
                "type": self.game_type,
            }
        )
        self._add_common_fields(home, away, comps)
        self._add_ranks(home, away)
        self._add_odds(comps)

    def _build_in_game(self):
        home, away, comps = self._base_team_info()
        self.obj.update(
            {
                "home": home["team"]["abbreviation"],
                "home_site": home["team"]["links"][0]["href"],
                "home_mascot": home["team"]["name"],
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
        self._add_ranks(home, away)

    def _build_post_game(self):
        self._build_in_game()


def create_base_obj_basketball(input_list, game_type):
    return [BasketballBaseObject(raw, game_type).to_dict() for raw in input_list]
