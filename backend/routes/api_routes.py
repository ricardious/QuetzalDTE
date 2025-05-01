from flask import Blueprint, request, jsonify
from controllers.dte_controller import DTEController

api_blueprint = Blueprint("api", __name__)
controller = DTEController()


@api_blueprint.route("/process", methods=["POST"])
def process_dte():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    xml_file = request.files["file"]
    if xml_file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    result = controller.process_requests(xml_file)
    return jsonify(result), 200


@api_blueprint.route("/authorizations", methods=["GET"])
def list_authorizations():
    data = controller.get_authorizations()
    return jsonify(data), 200


@api_blueprint.route("/summary/vat", methods=["GET"])
def vat_summary():
    date = request.args.get("date")
    if not date:
        return jsonify({"error": "Missing required parameter: date"}), 400

    summary = controller.get_vat_summary_by_date(date)
    return jsonify(summary), 200


@api_blueprint.route("/summary/range", methods=["GET"])
def range_summary():
    start = request.args.get("start")
    end = request.args.get("end")
    mode = request.args.get("mode", "total")
    if not start or not end:
        return jsonify({"error": "Missing required parameters: start and end"}), 400

    summary = controller.get_summary_by_range(start, end, mode)
    return jsonify(summary), 200


@api_blueprint.route("/reset", methods=["POST"])
def reset_system():
    controller.reset()
    return jsonify({"message": "System reset successfully"}), 200
