from flask import Blueprint, request, jsonify
from app.services.factcheck_service import FactCheckService

factcheck_bp = Blueprint("factcheck", __name__)
service = FactCheckService()


@factcheck_bp.route("", methods=["POST"])
def check_claim():
    """POST /api/v1/factcheck — AI-powered claim verification."""
    data = request.get_json()
    if not data or not data.get("claim"):
        return jsonify({"error": "Request body must include 'claim' field"}), 400

    claim = data["claim"].strip()
    if len(claim) < 5:
        return jsonify({"error": "Claim must be at least 5 characters"}), 400
    if len(claim) > 500:
        return jsonify({"error": "Claim must be under 500 characters"}), 400

    result = service.check_claim(claim)
    status_code = 200 if not result.error else 207
    return jsonify(result.to_dict()), status_code


@factcheck_bp.route("/batch", methods=["POST"])
def check_batch():
    """POST /api/v1/factcheck/batch — Check multiple claims at once."""
    data = request.get_json()
    if not data or not isinstance(data.get("claims"), list):
        return jsonify({"error": "Request body must include 'claims' array"}), 400

    claims = data["claims"][:5]  # Limit to 5 per batch
    results = [service.check_claim(c).to_dict() for c in claims if isinstance(c, str)]
    return jsonify({"results": results, "count": len(results)}), 200
