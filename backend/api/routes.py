"""HTTP routes for RepoIntel analysis."""

from fastapi import APIRouter, HTTPException
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
    try:
        repository, findings, classification, score = run_pipeline(
            request.url,
        )
    except ValueError as error:
        if str(error) == "Invalid GitHub repository URL.":
            raise HTTPException(
                status_code=400,
                detail=str(error),
            ) from error
        raise

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
