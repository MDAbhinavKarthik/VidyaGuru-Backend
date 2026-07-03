"""
Integrity & Anti-Cheat API Endpoints (v1)

Canonical endpoint definitions for:
- Submission analysis and integrity verification
- Anti-cheat detection and response
- User integrity profile management
"""

from datetime import datetime, timezone
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from core.dependencies import get_current_user, get_current_admin_user
from models.user import User
from models.anti_cheat import (
    SubmissionAnalysis,
    VerificationChallenge,
    UserIntegrityProfile,
    SuspiciousActivityLog,
    SuspicionLevel,
    VerificationStatus
)
from services.anti_cheat.schemas import (
    SubmissionWithMetrics,
    SubmissionAnalysisResponse,
    SubmissionAnalysisResult,
    VerificationChallengeResponse,
    VerificationSubmitRequest,
    VerificationResultResponse,
    VerificationTypeEnum,
    IntegrityProfileResponse,
    IntegrityStatsResponse,
    VerificationHistoryItem,
    SuspiciousActivityResponse,
    ActivityAlertResponse,
    GenuineLearnerReminder,
    IntegrityAnalyticsSummary,
    FlaggedSubmissionResponse,
    REMINDER_MESSAGES,
    SuspicionLevelEnum,
    VerificationStatusEnum,
    IntegrityLevelEnum
)
from services.anti_cheat.service import (
    SubmissionAnalyzer,
    VerificationService,
    IntegrityService
)

router = APIRouter(prefix="/integrity", tags=["Integrity & Anti-Cheat"])


# ============================================================================
# Submission Analysis Endpoints
# ============================================================================

@router.post(
    "/analyze",
    response_model=SubmissionAnalysisResponse,
    summary="Analyze a submission for suspicious behavior",
    description="""
    Analyzes a task submission for potential cheating indicators.
    
    Detection methods:
    - Large paste detection
    - Rapid submission timing
    - Similar/identical answer matching
    - Typing pattern anomalies
    - Skill consistency checking
    
    Returns analysis results and may include a verification challenge if needed.
    """
)
async def analyze_submission(
    submission: SubmissionWithMetrics,
    task_id: UUID = Query(..., description="ID of the task being submitted"),
    expected_time_seconds: int = Query(600, description="Expected completion time"),
    task_type: str = Query("general", description="Type of task"),
    task_difficulty: str = Query("intermediate", description="Task difficulty"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Analyze submission and return integrity assessment"""
    analyzer = SubmissionAnalyzer(db)
    
    # Perform analysis
    result = await analyzer.analyze_submission(
        submission=submission,
        task_id=task_id,
        expected_time_seconds=expected_time_seconds,
        task_type=task_type,
        task_difficulty=task_difficulty
    )
    
    # Update user's integrity profile
    integrity_service = IntegrityService(db)
    await integrity_service.update_on_submission(
        user_id=current_user.id,
        was_flagged=result.suspicion_level in [SuspicionLevelEnum.HIGH, SuspicionLevelEnum.CRITICAL],
        suspicion_score=result.suspicion_score
    )
    
    # Generate verification challenge if needed
    verification = None
    user_message = None
    
    if result.requires_verification:
        verification_service = VerificationService(db)
        verification = await verification_service.create_challenge(
            analysis_id=result.submission_analysis_id,
            user_id=current_user.id,
            verification_type=result.recommended_verification_type or VerificationTypeEnum.FOLLOW_UP_QUESTION,
            original_content=submission.content,
            task_context={
                "task_id": str(task_id),
                "task_type": task_type,
                "difficulty": task_difficulty
            }
        )
        
        # Get polite reminder message
        reminder = await integrity_service.get_reminder_message(
            user_id=current_user.id,
            suspicion_type=result.indicators[0].type if result.indicators else None
        )
        user_message = f"{reminder.title}\n\n{reminder.message}\n\n{reminder.encouragement}"
        
        # Log suspicious activity
        if result.indicators:
            for indicator in result.indicators:
                await integrity_service.log_suspicious_activity(
                    user_id=current_user.id,
                    analysis_id=result.submission_analysis_id,
                    suspicion_type=indicator.type,
                    severity=indicator.severity,
                    description=indicator.description,
                    evidence=indicator.evidence
                )
    
    return SubmissionAnalysisResponse(
        analysis=result,
        verification_challenge=verification,
        user_message=user_message
    )


@router.get(
    "/analysis/{analysis_id}",
    response_model=SubmissionAnalysisResult,
    summary="Get submission analysis details"
)
async def get_analysis(
    analysis_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific submission analysis"""
    analysis = await db.get(SubmissionAnalysis, analysis_id)
    
    if not analysis:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found"
        )
    
    # Users can only view their own analyses
    if analysis.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return SubmissionAnalysisResult(
        submission_analysis_id=analysis.id,
        task_assignment_id=analysis.task_assignment_id,
        suspicion_level=SuspicionLevelEnum(analysis.suspicion_level.value),
        suspicion_score=analysis.suspicion_score,
        requires_verification=analysis.requires_verification,
        indicators=[],
        summary=f"Suspicion level: {analysis.suspicion_level.value}"
    )


# ============================================================================
# Verification Challenge Endpoints
# ============================================================================

@router.get(
    "/verification/pending",
    response_model=List[VerificationChallengeResponse],
    summary="Get pending verification challenges"
)
async def get_pending_verifications(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all pending verification challenges for the current user"""
    result = await db.execute(
        select(VerificationChallenge)
        .where(
            and_(
                VerificationChallenge.user_id == current_user.id,
                VerificationChallenge.status.in_([
                    VerificationStatus.PENDING,
                    VerificationStatus.IN_PROGRESS
                ]),
                VerificationChallenge.expires_at > datetime.now(timezone.utc)
            )
        )
        .order_by(VerificationChallenge.created_at)
    )
    challenges = result.scalars().all()
    
    return [
        VerificationChallengeResponse(
            id=c.id,
            verification_type=VerificationTypeEnum(c.verification_type.value),
            prompt=c.challenge_prompt,
            context=c.challenge_context,
            original_code=c.original_code,
            min_response_length=c.min_response_length,
            expires_at=c.expires_at,
            attempt_number=c.attempt_number,
            max_attempts=c.max_attempts
        )
        for c in challenges
    ]


@router.get(
    "/verification/{challenge_id}",
    response_model=VerificationChallengeResponse,
    summary="Get verification challenge details"
)
async def get_verification_challenge(
    challenge_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific verification challenge"""
    challenge = await db.get(VerificationChallenge, challenge_id)
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    if challenge.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Check expiry
    if datetime.now(timezone.utc) > challenge.expires_at:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="This verification challenge has expired"
        )
    
    return VerificationChallengeResponse(
        id=challenge.id,
        verification_type=VerificationTypeEnum(challenge.verification_type.value),
        prompt=challenge.challenge_prompt,
        context=challenge.challenge_context,
        original_code=challenge.original_code,
        min_response_length=challenge.min_response_length,
        expires_at=challenge.expires_at,
        attempt_number=challenge.attempt_number,
        max_attempts=challenge.max_attempts
    )


@router.post(
    "/verification/{challenge_id}/submit",
    response_model=VerificationResultResponse,
    summary="Submit response to verification challenge"
)
async def submit_verification(
    challenge_id: UUID,
    request: VerificationSubmitRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit a response to a verification challenge"""
    challenge = await db.get(VerificationChallenge, challenge_id)
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Challenge not found"
        )
    
    if challenge.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    if challenge.status in [VerificationStatus.PASSED, VerificationStatus.EXPIRED]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Challenge is already {challenge.status.value}"
        )
    
    verification_service = VerificationService(db)
    return await verification_service.evaluate_response(
        challenge_id=challenge_id,
        response=request.response,
        typing_metrics=request.typing_metrics
    )


# ============================================================================
# User Integrity Profile Endpoints
# ============================================================================

@router.get(
    "/profile",
    response_model=IntegrityProfileResponse,
    summary="Get your integrity profile"
)
async def get_my_integrity_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the current user's integrity profile"""
    integrity_service = IntegrityService(db)
    profile = await integrity_service.get_or_create_profile(current_user.id)
    
    # Calculate verification pass rate
    total_verifications = profile.verifications_passed + profile.verifications_failed
    pass_rate = (
        profile.verifications_passed / total_verifications 
        if total_verifications > 0 else 1.0
    )
    
    return IntegrityProfileResponse(
        user_id=profile.user_id,
        trust_score=profile.trust_score,
        integrity_level=IntegrityLevelEnum(profile.integrity_level),
        total_submissions=profile.total_submissions,
        flagged_submissions=profile.flagged_submissions,
        verification_pass_rate=pass_rate,
        is_restricted=profile.is_restricted,
        restriction_reason=profile.restriction_reason,
    )


@router.get(
    "/stats",
    response_model=IntegrityStatsResponse,
    summary="Get integrity statistics"
)
async def get_integrity_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get detailed integrity statistics for the current user"""
    integrity_service = IntegrityService(db)
    return await integrity_service.get_stats(current_user.id)


# ============================================================================
# Admin Endpoints
# ============================================================================

@router.get(
    "/admin/flagged-submissions",
    response_model=List[FlaggedSubmissionResponse],
    summary="Get flagged submissions (admin only)"
)
async def get_flagged_submissions(
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all flagged submissions for admin review"""
    result = await db.execute(
        select(SubmissionAnalysis)
        .where(SubmissionAnalysis.is_flagged == True)
        .order_by(desc(SubmissionAnalysis.created_at))
        .limit(page_size)
        .offset((page - 1) * page_size)
    )
    submissions = result.scalars().all()
    
    return [
        FlaggedSubmissionResponse(
            analysis_id=s.id,
            user_id=s.user_id,
            suspicion_score=s.suspicion_score,
            suspicion_level=SuspicionLevelEnum(s.suspicion_level.value),
            flagged_at=s.created_at,
            reviewed=s.reviewed_by_admin,
            admin_notes=s.admin_notes,
        )
        for s in submissions
    ]


@router.post(
    "/admin/review/{analysis_id}",
    summary="Admin review of flagged submission"
)
async def admin_review_submission(
    analysis_id: UUID,
    action: str = Query(..., regex="^(approve|escalate|dismiss)$"),
    notes: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Admin review and action on flagged submission"""
    analysis = await db.get(SubmissionAnalysis, analysis_id)
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis.reviewed_by_admin = True
    analysis.admin_notes = notes
    
    if action == "approve":
        analysis.is_flagged = False
    elif action == "escalate":
        # Mark for further investigation
        pass
    
    await db.commit()
    
    return {
        "message": f"Submission {action}ed by admin",
        "analysis_id": str(analysis_id)
    }


# Delegate advanced/admin anti-cheat routes to the modular engine router
from services.anti_cheat.api import router as modular_integrity_router
for _route in modular_integrity_router.routes:
    if not any(r.path == _route.path and getattr(r, "methods", None) == getattr(_route, "methods", None) for r in router.routes):
        router.routes.append(_route)

