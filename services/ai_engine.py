import json
import os

from services.db import (
    get_organisation,
    save_analysis,
    get_analysis
)

from google import genai


SYSTEM_PROMPT = """
You are an enterprise transformation strategy analyst.

Use ONLY the organisation information and external research supplied to you.

Do not invent external facts, citations, statistics or URLs.

If evidence is insufficient, explicitly say so.

Produce practical, evidence-linked and prioritised transformation intelligence.

The strategy must connect:

Business Situation
→ External Change
→ Strategic Issues
→ Transformation Opportunities
→ Priorities
→ Initiatives
→ Outcomes
"""


def _client():
    return genai.Client(
        api_key=os.getenv("GEMINI_API_KEY")
    )


def _clean_json(text):
    """
    Removes markdown code fences if Gemini returns JSON inside ```json ... ```
    """
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    return text.strip()


def analyse_strategy(org_id, research):

    # First check whether an analysis is already saved.
    existing_analysis = get_analysis(org_id)

    if existing_analysis:
        return existing_analysis

    org = get_organisation(org_id)

    prompt = f"""
Organisation:
{json.dumps(org, indent=2)}

External research:
{json.dumps(research, indent=2)}

Analyse the organisation using ONLY the information above.

Return ONLY valid JSON.

Use exactly this structure:

{{
  "diagnosis": "...",

  "strategic_issues": [
    {{
      "issue": "...",
      "why": "...",
      "evidence": ["..."]
    }}
  ],

  "opportunities": [
    {{
      "name": "...",
      "rationale": "..."
    }}
  ],

  "priorities": [
    {{
      "rank": 1,
      "opportunity": "...",
      "impact": 1,
      "urgency": 1,
      "effort": 1
    }}
  ],

  "initiatives": [
    {{
      "initiative": "...",
      "purpose": "..."
    }}
  ],

  "outcomes": [
    "..."
  ]
}}

Rules:

1. Scores must be integers from 1 to 10.
2. Rank opportunities using business value, urgency, effort and evidence strength.
3. Evidence must come from the supplied organisation information or research.
4. Do not create fake sources.
5. Do not create fake statistics.
6. Do not create fake URLs.
7. If evidence is insufficient, clearly state that.
8. Recommendations must be practical.
"""

    if not os.getenv("GEMINI_API_KEY"):
        analysis = demo_analysis(org, research)
        save_analysis(org_id, analysis)
        return analysis

    client = _client()

    response = client.models.generate_content(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-flash-latest"
        ),
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "response_mime_type": "application/json"
        }
    )

    text = _clean_json(response.text)

    analysis = json.loads(text)

    # Save the generated AI intelligence permanently.
    save_analysis(org_id, analysis)

    return analysis


def answer_question(question, analysis):

    if not os.getenv("GEMINI_API_KEY"):
        return (
            "Gemini API is not configured. "
            "Set GEMINI_API_KEY in the .env file."
        )

    client = _client()

    prompt = f"""
Question:
{question}

Application intelligence:
{json.dumps(analysis, indent=2)}

Answer the question using ONLY the application intelligence.

Clearly explain:

1. Finding
2. Evidence
3. Recommendation
4. First action

Do not invent facts or evidence.
"""

    response = client.models.generate_content(
        model=os.getenv(
            "GEMINI_MODEL",
            "gemini-flash-latest"
        ),
        contents=prompt,
        config={
            "system_instruction": SYSTEM_PROMPT
        }
    )

    return response.text


def demo_analysis(org, research):

    return {
        "diagnosis": (
            f"{org.get('name', 'The organisation')} "
            "should focus on transformation opportunities "
            "linked to its stated business situation and "
            "available research evidence."
        ),

        "strategic_issues": [
            {
                "issue": "Operational efficiency",
                "why": (
                    "The organisation's business situation "
                    "indicates a need to improve operational performance."
                ),
                "evidence": [
                    "Organisation-provided business situation"
                ]
            },
            {
                "issue": "Customer and digital transformation",
                "why": (
                    "The stated objectives indicate a need "
                    "to improve customer experience and digital capability."
                ),
                "evidence": [
                    "Organisation-provided business objectives"
                ]
            }
        ],

        "opportunities": [
            {
                "name": "Data-driven operations optimisation",
                "rationale": (
                    "Use available organisational data "
                    "to improve planning and operational decisions."
                )
            },
            {
                "name": "Customer and omnichannel improvement",
                "rationale": (
                    "Connect customer and digital information "
                    "to improve the customer experience."
                )
            }
        ],

        "priorities": [
            {
                "rank": 1,
                "opportunity": "Data-driven operations optimisation",
                "impact": 9,
                "urgency": 8,
                "effort": 5
            },
            {
                "rank": 2,
                "opportunity": "Customer and omnichannel improvement",
                "impact": 8,
                "urgency": 7,
                "effort": 7
            }
        ],

        "initiatives": [
            {
                "initiative": "Data assessment and pilot",
                "purpose": (
                    "Assess available data and test a high-value "
                    "transformation use case."
                )
            },
            {
                "initiative": "Customer journey analysis",
                "purpose": (
                    "Identify high-value customer experience "
                    "improvements."
                )
            }
        ],

        "outcomes": [
            "Better evidence-based decision making",
            "Improved operational efficiency",
            "Improved customer experience"
        ]
    }