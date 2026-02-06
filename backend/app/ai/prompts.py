from typing import List, Optional

INCIDENT_ANALYSIS_PROMPT = """You are an incident analysis assistant for a trading/fintech platform (like Deriv).

Analyze the following logs and incident reports:

{logs}

{similar_context}

Provide:
1. Short incident summary
2. Likely root cause
3. Severity level (P1 critical → P4 minor)
4. Suggested responsible team
5. Recommended next action

Respond ONLY in the following JSON format (no markdown, no extra text):
{{
  "summary": "...",
  "root_cause": "...",
  "severity_level": "P1|P2|P3|P4",
  "recommended_owner": "...",
  "next_steps": "..."
}}

Keep output deterministic and concise. Severity guidelines:
- P1: Complete service outage, data loss, security breach, trading halted
- P2: Major feature degraded, significant latency, partial outage
- P3: Minor feature issue, intermittent errors, workaround available
- P4: Cosmetic issues, minor warnings, informational alerts
"""


def build_analysis_prompt(
    logs: List[str],
    similar_incidents: Optional[List[str]] = None,
) -> str:
    """Build the full analysis prompt with logs and optional similar incidents."""
    logs_text = "\n".join(f"- {log}" for log in logs)

    similar_context = ""
    if similar_incidents:
        similar_text = "\n".join(f"- {inc}" for inc in similar_incidents)
        similar_context = f"\nHistorically similar incidents found:\n{similar_text}\n"

    return INCIDENT_ANALYSIS_PROMPT.format(
        logs=logs_text,
        similar_context=similar_context,
    )
