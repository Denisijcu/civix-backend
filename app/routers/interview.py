from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import ai_service

router = APIRouter(prefix="/api/interview", tags=["Interview"])

class EvaluateRequest(BaseModel):
    question_text: str
    user_answer: str
    official_context: str
    current_stress_level: int

class EvaluateResponse(BaseModel):
    is_correct: bool
    explanation: str
    new_stress_level: int

@router.post("/evaluate", response_model=EvaluateResponse)
async def evaluate_interview_answer(request: EvaluateRequest):
    try:
        # 1. Llamamos a Claude
        ai_result = ai_service.evaluate_answer(
            question=request.question_text,
            user_answer=request.user_answer,
            official_context=request.official_context,
            current_stress=request.current_stress_level
        )

        # 2. Calculamos el nuevo nivel de estrés (manteniéndolo entre 1 y 10)
        adjustment = ai_result.get("stress_adjustment", 0)
        new_stress = request.current_stress_level + adjustment
        new_stress = max(1, min(10, new_stress)) # Limitar entre 1 y 10

        # 3. Devolvemos la respuesta al Frontend
        return EvaluateResponse(
            is_correct=ai_result["is_correct"],
            explanation=ai_result["explanation"],
            new_stress_level=new_stress
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))