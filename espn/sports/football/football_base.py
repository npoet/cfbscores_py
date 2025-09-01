from espn.utils import convert_time
from espn.sports import SportsBaseObject


class FootballBaseObject(SportsBaseObject):
    def _build_pre_game(self):
        if "TBD" in self.raw.get("shortName", "") or "TBA" in self.raw.get("shortName", ""):
            return
        home, away, comps = self._base_team_info()
        self.obj.update({
            "home_id": home["team"]["location"],
            "home": home["team"]["abbreviation"],
            "home_site": home["team"]["links"][0]["href"],
            "home_mascot": home["team"]["name"],
            "away_id": away["team"]["location"],
            "away": away["team"]["abbreviation"],
            "away_site": away["team"]["links"][0]["href"],
            "away_mascot": away["team"]["name"],
            "time": convert_time(self.raw["date"]),
            "date": self.raw["date"],
            "type": self.game_type,
        })
        self._add_common_fields(home, away, comps)
        self._add_ranks(home, away)
        self._add_odds(comps)
        self._add_leaders(home, away)

    def _build_in_game(self):
        home, away, comps = self._base_team_info()
        self.obj.update({
            "home_id": home["team"]["location"],
            "home": home["team"]["abbreviation"],
            "home_site": home["team"]["links"][0]["href"],
            "home_mascot": home["team"]["name"],
            "away_id": away["team"]["location"],
            "away": away["team"]["abbreviation"],
            "away_site": away["team"]["links"][0]["href"],
            "away_mascot": away["team"]["name"],
            "home_score": home.get("score"),
            "away_score": away.get("score"),
            "time": self.raw["status"]["type"]["shortDetail"],
            "date": self.raw["date"],
            "type": self.game_type,
        })
        self._add_common_fields(home, away, comps)
        self._add_ranks(home, away)
        self._add_possession(comps, home)
        self._add_global_leaders(comps)
        self._add_last_play(comps)
        self._add_win_prob(comps)

    def _build_post_game(self):
        home, away, comps = self._base_team_info()
        self.obj.update({
            "home_id": home["team"]["location"],
            "home": home["team"]["abbreviation"],
            "home_site": home["team"]["links"][0]["href"],
            "home_mascot": home["team"]["name"],
            "away_id": away["team"]["location"],
            "away": away["team"]["abbreviation"],
            "away_site": away["team"]["links"][0]["href"],
            "away_mascot": away["team"]["name"],
            "home_score": home.get("score"),
            "away_score": away.get("score"),
            "time": self.raw["status"]["type"]["shortDetail"],
            "date": self.raw["date"],
            "type": self.game_type,
        })
        self._add_common_fields(home, away, comps)
        self._add_ranks(home, away)
        self._add_global_leaders(comps)
        self._add_team_leaders(home, away)
        self._add_headline(comps)
        self._add_links()

    # --- football-specific helpers ---
    def _add_leaders(self, home, away):
        for side, label in [(home, "home"), (away, "away")]:
            try:
                pas = side["leaders"][0]["leaders"][0]
                rush = side["leaders"][1]["leaders"][0]
                rec = side["leaders"][2]["leaders"][0]
                self.obj[f"{label}_pass"] = self._fmt_leader(pas)
                self.obj[f"{label}_rush"] = self._fmt_leader(rush)
                self.obj[f"{label}_rec"] = self._fmt_leader(rec)
            except (KeyError, IndexError):
                pass

    def _add_possession(self, comps, home):
        try:
            home_id = home["id"]
            poss_id = comps["situation"]["possession"]
            ball_on = comps["situation"]["possessionText"]
            self.obj["possession"] = "home" if poss_id == home_id else "away"
            self.obj["ball_on"] = ball_on
        except KeyError:
            self.obj["possession"] = ""
            self.obj["ball_on"] = ""

    def _add_global_leaders(self, comps):
        try:
            pas, rush, rec = [comps["leaders"][i]["leaders"][0] for i in range(3)]
            self.obj["pass_leader"] = self._fmt_leader(pas, with_name=True)
            self.obj["rush_leader"] = self._fmt_leader(rush, with_name=True)
            self.obj["rec_leader"] = self._fmt_leader(rec, with_name=True)
        except (KeyError, IndexError):
            pass

    def _add_last_play(self, comps):
        try:
            self.obj["last_play"] = comps["situation"]["lastPlay"]["text"]
            self.obj["down_distance"] = comps["situation"]["downDistanceText"]
        except KeyError:
            pass

    def _add_win_prob(self, comps):
        try:
            prob = comps["situation"]["lastPlay"]["probability"]
            home_prob, away_prob = prob["homeWinPercentage"], prob["awayWinPercentage"]
            if home_prob >= away_prob:
                self.obj["win_prob"] = f"{self.obj['home']} {round(home_prob*100, 2)}%"
            else:
                self.obj["win_prob"] = f"{self.obj['away']} {round(away_prob*100, 2)}%"
        except KeyError:
            pass

    def _add_team_leaders(self, home, away):
        self._add_leaders(home, away)

    def _add_links(self):
        try:
            links = self.raw.get("links", [])
            self.obj["gamecast"] = links[0]["href"]
            self.obj["box_score"] = links[1]["href"]
            self.obj["highlights"] = links[2]["href"]
        except (KeyError, IndexError):
            pass

    def _add_headline(self, comps):
        try:
            self.obj["headline"] = comps["headlines"][0]["shortLinkText"]
            self.obj["description"] = comps["headlines"][0]["description"][1:]
        except (KeyError, IndexError):
            pass

    @staticmethod
    def _fmt_leader(ld, with_name=False):
        if with_name:
            return f"{ld['athlete']['shortName']} {ld['displayValue']}"
        return f"{ld['displayValue']}"
