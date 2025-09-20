class SportsBaseObject:
    def __init__(self, raw_data: dict, game_type: str):
        self.raw = raw_data
        self.game_type = game_type
        self.obj = {"game_id": self.raw.get("id")}
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

    def _add_common_fields(self, home, away, comps):
        self.obj["home_logo"] = home["team"].get("logo") + "&h=104&w=104"
        self.obj["away_logo"] = away["team"].get("logo") + "&h=104&w=104"
        self.obj["home_record"] = self._safe_get(home, ["records", 0, "summary"], "")
        self.obj["away_record"] = self._safe_get(away, ["records", 0, "summary"], "")
        try:
            short_name = comps["geoBroadcasts"][0]["media"]["shortName"]
            if short_name == "The CW Network":
                self.obj["tv"] = "The CW"
            elif short_name == "NEC Front Row":
                self.obj["tv"] = "NEC Net"
            elif short_name == "Scripps Sports":
                self.obj["tv"] = "Scripps"
            elif short_name.endswith("Network"):
                self.obj["tv"] = short_name.replace("Network", "Net")
            else:
                self.obj["tv"] = short_name
        except (KeyError, IndexError):
            self.obj["tv"] = "Off Air"

    def _add_odds(self, comps, index: int = 0):
        try:
            self.obj["odds"] = f"{self.game_type} | " + comps["odds"][index]["details"]
        except (KeyError, IndexError):
            self.obj["odds"] = f"{self.game_type} | No Line"

    def _add_ranks(self, home, away):
        try:
            if home["curatedRank"]["current"] <= 25:
                self.obj["home"] = (
                    f"#{home['curatedRank']['current']} {self.obj['home']}"
                )
        except KeyError:
            pass
        try:
            if away["curatedRank"]["current"] <= 25:
                self.obj["away"] = (
                    f"#{away['curatedRank']['current']} {self.obj['away']}"
                )
        except KeyError:
            pass

    @staticmethod
    def _safe_get(d, path, default=None):
        try:
            for p in path:
                d = d[p]
            return d
        except (KeyError, IndexError, TypeError):
            return default

    def to_dict(self):
        return self.obj

    # abstract methods for subclasses
    def _build_pre_game(self):
        raise NotImplementedError

    def _build_in_game(self):
        raise NotImplementedError

    def _build_post_game(self):
        raise NotImplementedError
