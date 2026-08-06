"""HTTP routes for RepoIntel analysis."""

from fastapi import APIRouter
from api.schemas import (
    AnalyzeRequest,
    AnalysisResponse,
    FindingResponse,
    OverallScoreResponse,
    ProjectClassificationResponse,
    RepositoryResponse,
)
from api.services import run_pipeline


router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
def analyze_repository(request: AnalyzeRequest) -> AnalysisResponse:
    repository, findings, classification, score = run_pipeline(
        request.url,
    )

    return AnalysisResponse(
        repository=RepositoryResponse.model_validate(repository),
        findings=[
            FindingResponse.model_validate(finding)
            for finding in findings
        ],
        classification=ProjectClassificationResponse.model_validate(
            classification,
        ),
        score=OverallScoreResponse.model_validate(score),
    )
