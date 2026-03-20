from fastapi import APIRouter

from app.core.config import settings
from app.schemas.pet import GrowthRuleResponse
from app.services.growth_service import GrowthService

router = APIRouter(prefix='/growth-rules')


@router.get('', response_model=GrowthRuleResponse)
def get_growth_rules() -> GrowthRuleResponse:
    return GrowthRuleResponse(points_per_level=settings.points_per_level, stages=GrowthService.get_rule_payload())
