from fastapi import APIRouter
from .teams_service import TeamsService, get_team_season

router = APIRouter()
service = TeamsService()


@router.get("/team/{team_id}")
async def get_info(team_id: str):
    """Get team ratings page (SP+, Elo, FPI, SRS)."""
    return service.get_team_info(team_id)


@router.get("/season/{team_id}")
def get_season(team_id: str):
    """Get season schedule and results for a given team."""
    return get_team_season(team_id)


@router.get("/record/{team_id}")
async def get_records(team_id: str):
    """Get record breakdowns (expected wins, conf, home, away)."""
    return service.get_team_records(team_id)
