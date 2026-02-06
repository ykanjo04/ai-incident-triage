import json
import os
import re
from typing import List, Optional

import google.generativeai as genai

from app.ai.prompts import build_analysis_prompt
from app.models.incident import IncidentAnalysis

# Configure the Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"


def extract_json_from_response(text: str) -> dict:
    """Extract JSON from LLM response, handling markdown code blocks."""
    # Try direct JSON parse first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting from markdown code block
    json_match = re.search(r"```(?:json)?\s*\n(.*?)\n```", text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Try finding the outermost JSON object
    # Find the first { and last } to extract the full JSON
    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        try:
            return json.loads(text[first_brace:last_brace + 1])
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract valid JSON from response: {text[:200]}")


def analyze_incident(
    logs: List[str],
    similar_incidents: Optional[List[str]] = None,
) -> IncidentAnalysis:
    """Analyze an incident using Gemini LLM.

    Args:
        logs: List of log messages to analyze
        similar_incidents: Optional list of similar past incidents for context

    Returns:
        Structured IncidentAnalysis result
    """
    prompt = build_analysis_prompt(logs, similar_incidents)

    model = genai.GenerativeModel(MODEL_NAME)

    # Attempt analysis with retry
    last_error = None
    for attempt in range(3):
        try:
            response = model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    temperature=0.1,  # Low temperature for deterministic output
                    max_output_tokens=4096,
                    response_mime_type="application/json",
                ),
            )

            result_dict = extract_json_from_response(response.text)

            # Validate and return
            return IncidentAnalysis(
                summary=result_dict.get("summary", "Unable to generate summary"),
                root_cause=result_dict.get("root_cause", "Unable to determine root cause"),
                severity_level=result_dict.get("severity_level", "P3"),
                recommended_owner=result_dict.get("recommended_owner", "Engineering On-Call"),
                next_steps=result_dict.get("next_steps", "Investigate further"),
            )

        except Exception as e:
            last_error = e
            print(f"Analysis attempt {attempt + 1} failed: {e}")
            continue

    # Fallback response if all retries fail
    print(f"All analysis attempts failed. Last error: {last_error}")
    return IncidentAnalysis(
        summary="Analysis could not be completed due to API error",
        root_cause=f"LLM analysis failed: {str(last_error)}",
        severity_level="P3",
        recommended_owner="Engineering On-Call",
        next_steps="Retry analysis or perform manual triage",
    )
