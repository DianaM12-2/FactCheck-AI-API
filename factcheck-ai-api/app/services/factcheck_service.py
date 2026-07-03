import os
import json
import requests
from dataclasses import dataclass
from typing import Optional


@dataclass
class FactCheckResult:
    """Result of an AI-powered fact check."""
    claim: str
    verdict: str           # "TRUE", "FALSE", "UNCERTAIN", "MISLEADING"
    confidence: float      # 0.0 - 1.0
    explanation: str
    sources_consulted: int
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "claim":              self.claim,
            "verdict":            self.verdict,
            "confidence":         self.confidence,
            "confidence_percent": f"{self.confidence * 100:.1f}%",
            "explanation":        self.explanation,
            "sources_consulted":  self.sources_consulted,
            "error":              self.error,
        }


class FactCheckService:
    """
    AI-powered fact-checking service using the Gemini API.
    Demonstrates REST API integration, error handling, and JSON parsing.
    """

    GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    SYSTEM_PROMPT = """You are a fact-checking assistant. Analyze the given claim and respond ONLY with a JSON object in this exact format:
{
  "verdict": "TRUE" | "FALSE" | "UNCERTAIN" | "MISLEADING",
  "confidence": <float between 0 and 1>,
  "explanation": "<one clear sentence explaining your verdict>"
}
Do not include any text outside the JSON object."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")

    def check_claim(self, claim: str) -> FactCheckResult:
        """
        Send a claim to Gemini API and return a structured fact-check result.
        Falls back to mock response if API key is not configured.
        """
        if not self.api_key:
            return self._mock_response(claim)

        try:
            response = requests.post(
                f"{self.GEMINI_URL}?key={self.api_key}",
                json={
                    "contents": [{
                        "parts": [{
                            "text": f"{self.SYSTEM_PROMPT}\n\nClaim to check: {claim}"
                        }]
                    }]
                },
                timeout=10
            )
            response.raise_for_status()

            # Parse Gemini response
            raw_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(raw_text.strip())

            return FactCheckResult(
                claim=claim,
                verdict=parsed.get("verdict", "UNCERTAIN"),
                confidence=float(parsed.get("confidence", 0.5)),
                explanation=parsed.get("explanation", "Unable to determine."),
                sources_consulted=1,
            )

        except requests.exceptions.Timeout:
            return FactCheckResult(claim=claim, verdict="UNCERTAIN", confidence=0.0,
                                   explanation="Request timed out.", sources_consulted=0,
                                   error="API timeout")
        except requests.exceptions.RequestException as e:
            return FactCheckResult(claim=claim, verdict="UNCERTAIN", confidence=0.0,
                                   explanation="API error occurred.", sources_consulted=0,
                                   error=str(e))
        except (json.JSONDecodeError, KeyError) as e:
            return FactCheckResult(claim=claim, verdict="UNCERTAIN", confidence=0.0,
                                   explanation="Could not parse AI response.", sources_consulted=0,
                                   error=f"Parse error: {str(e)}")

    def _mock_response(self, claim: str) -> FactCheckResult:
        """Returns a demo response when no API key is set."""
        return FactCheckResult(
            claim=claim,
            verdict="UNCERTAIN",
            confidence=0.5,
            explanation="[DEMO MODE] Set GEMINI_API_KEY env variable for real AI fact-checking.",
            sources_consulted=0,
        )
