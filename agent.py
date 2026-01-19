import json
import os

from schemas import AnalysisRequest, AnalysisResult, Assumption, RiskLevel
from prompts import SYSTEM_PROMPT, build_user_prompt
import openrouterclient


def fallback_result(error: str = "") -> AnalysisResult:
    msg = "Unable to analyze the input. Please provide clear text to examine."
    if error:
        msg = f"Error: {error}"
    return AnalysisResult(
        assumptions=[],
        summary=msg
    )


def empty_input_result() -> AnalysisResult:
    return AnalysisResult(
        assumptions=[],
        summary="No text provided for analysis."
    )


def is_valid_input(text: str) -> bool:
    if not text:
        return False
    cleaned = text.strip()
    if len(cleaned) < 10:
        return False
    return True


def parse_model_response(raw: str) -> AnalysisResult:
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.startswith("```"):
            cleaned = cleaned[3:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]
        cleaned = cleaned.strip()
        
        data = json.loads(cleaned)
        assumptions = []
        
        for item in data.get("assumptions", []):
            risk = item.get("risk", "medium").lower()
            if risk not in ["low", "medium", "high"]:
                risk = "medium"
            
            confidence = item.get("confidence", 0.5)
            if not isinstance(confidence, (int, float)):
                confidence = 0.5
            confidence = max(0, min(1, float(confidence)))
            
            assumption = Assumption(
                text=str(item.get("text", "")),
                risk=RiskLevel(risk),
                confidence=confidence,
                explanation=str(item.get("explanation", "")),
                validation=str(item.get("validation", ""))
            )
            assumptions.append(assumption)
        
        summary = data.get("summary", "Analysis complete.")
        
        return AnalysisResult(assumptions=assumptions, summary=summary)
    
    except (json.JSONDecodeError, KeyError, ValueError):
        return fallback_result()


async def analyze(text: str) -> AnalysisResult:
    if not is_valid_input(text):
        return empty_input_result()
    
    try:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(text)}
        ]
        
        raw = openrouterclient.call(messages)
        result = parse_model_response(raw)
        return result
    
    except openrouterclient.ModelError as e:
        return fallback_result(f"Model error: {str(e)}")
    except Exception as e:
        return fallback_result(f"{type(e).__name__}: {str(e)}")
