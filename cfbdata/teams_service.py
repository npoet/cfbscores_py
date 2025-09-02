import os
from datetime import datetime
import cfbd
import requests


def get_team_season(team_id: str) -> list:
    """Get season schedule and results for a given team."""
    url = "https://api.collegefootballdata.com/games?year=2025&team=Michigan"

    payload = {}
    headers = {
        'Authorization': f'Bearer {os.environ["CFBD_API_KEY"]}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    resp_games = response.json()
    season = []

    for game in resp_games:
        obj = {
            "home": game["homeTeam"],
            "away": game["awayTeam"],
            "home_score": game["homePoints"],
            "away_score": game["awayPoints"],
            "date": datetime.fromisoformat(game["startDate"]).date(),
        }
        if game["notes"] is not None:
            obj["note"] = game["notes"]

        try:
            if game["homeTeam"].lower() == team_id.lower():
                obj["pg_win_prob"] = round(game["homePostgameWinProbability"], 4)
            elif game["awayTeam"].lower() == team_id.lower():
                obj["pg_win_prob"] = round(game["awayPostgameWinProbability"], 4)
        except (TypeError, AttributeError):
            obj["pg_win_prob"] = ""

        season.append(obj)

    return season


class TeamsService:
    def __init__(self, year: int = 2025):
        # init CFBD config
        config = cfbd.Configuration()
        config.api_key["Authorization"] = os.environ["CFBD_API_KEY"]
        config.api_key_prefix["Authorization"] = "Bearer"

        self.year = year
        self.ratings = cfbd.RatingsApi(cfbd.ApiClient(config))
        self.games = cfbd.GamesApi(cfbd.ApiClient(config))

    def get_team_info(self, team_id: str) -> dict:
        """Build team ratings page (SP+, Elo, FPI, SRS)."""
        resp_sp = self.ratings.get_sp_ratings(year=self.year)
        team_ranking_sp = [
            r.ranking for r in resp_sp if r.team.lower() == team_id.lower()
        ][0]
        resp_sp_team = self.ratings.get_sp_ratings(
            year=self.year, team=team_id.lower()
        )
        sp = resp_sp_team[0]

        return_data = {
            "sp_ovr_ranking": team_ranking_sp,
            "sp_ovr_rating": sp.rating,
            "sp_off_rating": sp.offense.rating,
            "sp_def_rating": sp.defense.rating,
        }

        # Elo
        resp_elo = self.ratings.get_elo_ratings(year=self.year, team=team_id.lower())
        return_data["elo_ovr_rating"] = resp_elo[0].elo

        # FPI
        resp_fpi = self.ratings.get_fpi_ratings(year=self.year, team=team_id.lower())
        fpi = resp_fpi[0]
        return_data.update(
            {
                "fpi_ovr_ranking": fpi.resume_ranks.fpi,
                "fpi_ovr_rating": fpi.fpi,
                "fpi_sos": fpi.resume_ranks.strength_of_schedule,
                "fpi_game_control": fpi.resume_ranks.game_control,
            }
        )

        # SRS
        resp_srs = self.ratings.get_srs_ratings(year=self.year, team=team_id.lower())
        try:
            srs = resp_srs[0]
            return_data["srs_ovr_rating"] = srs.rating
        except IndexError:
            pass

        return return_data

    def get_team_records(self, team_id: str) -> dict:
        """Return record breakdowns (expected wins, conf, home, away)."""
        resp_rec = self.games.get_team_records(year=self.year, team=team_id)[0]
        return {
            "exp_wins": resp_rec.expected_wins,
            "conference_wl": f"{resp_rec.conference_games.wins}-{resp_rec.conference_games.losses}",
            "home_wl": f"{resp_rec.home_games.wins}-{resp_rec.home_games.losses}",
            "away_wl": f"{resp_rec.away_games.wins}-{resp_rec.away_games.losses}",
        }
