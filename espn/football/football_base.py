from espn.utils import convert_time


class FootballBaseObject:
    def __init__(self, raw_data: dict, game_type: str):
        self.raw = raw_data
        self.game_type = game_type
        self.obj = {
            # include game id from espn for identifying duplicates (FBS vs FCS etc.)
            "game_id": self.raw.get("id")
        }

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
            "type": self.game_type
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
            "type": self.game_type
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
            "type": self.game_type
        })
        self._add_common_fields(home, away, comps)
        self._add_ranks(home, away)
        self._add_global_leaders(comps)
        self._add_team_leaders(home, away)
        self._add_links()

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
            self.obj["odds"] = f"{self.game_type} | " + comps["odds"][0]["details"]
        except (KeyError, IndexError):
            self.obj["odds"] = f"{self.game_type} | No Line"

    def _add_ranks(self, home, away):
        try:
            if home["curatedRank"]["current"] <= 25:
                self.obj["home"] = f"#{home['curatedRank']['current']} {self.obj['home']}"
        except KeyError:
            pass
        try:
            if away["curatedRank"]["current"] <= 25:
                self.obj["away"] = f"#{away['curatedRank']['current']} {self.obj['away']}"
        except KeyError:
            pass

    def _add_leaders(self, home, away):
        # team-specific leaders
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
        except KeyError:
            pass

    @staticmethod
    def _fmt_leader(ld, with_name=False):
        if with_name:
            return f"{ld['athlete']['shortName']} {ld['displayValue']}"
        return f"{ld['displayValue']}"

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
