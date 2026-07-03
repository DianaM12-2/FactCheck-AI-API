from flask import Blueprint, request, jsonify
from app.services.claims_service import ClaimsService

claims_bp = Blueprint("claims", __name__)
service = ClaimsService()


@claims_bp.route("", methods=["GET"])
def get_all():
    return jsonify(service.get_all()), 200


@claims_bp.route("/<claim_id>", methods=["GET"])
def get_one(claim_id):
    claim = service.get_by_id(claim_id)
    if not claim:
        return jsonify({"error": f"Claim {claim_id} not found"}), 404
    return jsonify(claim.to_dict()), 200


@claims_bp.route("", methods=["POST"])
def create():
    data = request.get_json()
    required = ["patient_name", "medication", "amount"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400
    try:
        claim = service.create(data)
        return jsonify(claim.to_dict()), 201
    except (ValueError, TypeError) as e:
        return jsonify({"error": str(e)}), 400


@claims_bp.route("/<claim_id>", methods=["DELETE"])
def delete(claim_id):
    if service.delete(claim_id):
        return "", 204
    return jsonify({"error": f"Claim {claim_id} not found"}), 404


@claims_bp.route("/flagged", methods=["GET"])
def get_flagged():
    return jsonify(service.get_flagged()), 200


@claims_bp.route("/analytics", methods=["GET"])
def analytics():
    return jsonify(service.get_analytics()), 200
