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
                "time": self.raw["status"]["type"]["shortDetail"],
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
        self._add_last_play(comps)
        self._add_win_prob(comps)

    def _build_post_game(self):
        self._build_in_game()

    def _add_last_play(self, comps):
        try:
            self.obj["last_play"] = comps["situation"]["lastPlay"]["text"]
            self.obj["down_distance"] = comps["situation"]["downDistanceText"]
            self.obj["short_down_distance"] = comps["situation"][
                "shortDownDistanceText"
            ]
        except KeyError:
            pass

    def _add_win_prob(self, comps):
        try:
            prob = comps["situation"]["lastPlay"]["probability"]
            home_prob, away_prob = prob["homeWinPercentage"], prob["awayWinPercentage"]
            if home_prob >= away_prob:
                self.obj["win_prob"] = f"{self.obj['home']} {round(home_prob * 100, 2)}%"
            else:
                self.obj["win_prob"] = f"{self.obj['away']} {round(away_prob * 100, 2)}%"
        except KeyError:
            pass

    def _add_leaders(self, home, away):
        for side, label in [(home, "home"), (away, "away")]:
            try:
                pts = side["leaders"][0]["leaders"][0]
                reb = side["leaders"][1]["leaders"][0]
                ast = side["leaders"][2]["leaders"][0]
                self.obj[f"{label}_pts_leader"] = self._fmt_leader(pts)
                self.obj[f"{label}_reb_leader"] = self._fmt_leader(reb)
                self.obj[f"{label}_ast_leader"] = self._fmt_leader(ast)
            except (KeyError, IndexError):
                pass

    @staticmethod
    def _fmt_leader(ld, with_name=False):
        if with_name:
            return f"{ld['athlete']['shortName']} {ld['displayValue']}"
        return f"{ld['displayValue']}"


def create_base_obj_basketball(input_list, game_type):
    return [BasketballBaseObject(raw, game_type).to_dict() for raw in input_list]
