'''This module wraps rest API to extract signature from
the database'''

from flask import Blueprint, send_from_directory, render_template, jsonify
from flask_server.models.signatures import get_fuzzable_signatures, get_isas, get_fuzzable_signatures_deprecated, get_test_signatures

signatures_bp = Blueprint('signatures', __name__)


@signatures_bp.route("/api/signatures/fuzzable", methods=['GET'])
def get_fuzzable():
    signatures = get_fuzzable_signatures()
    return jsonify(signatures)

@signatures_bp.route("/api/signatures/fuzzable-old", methods=['GET'])
def get_fuzzable_deprecated():
    signatures = get_fuzzable_signatures_deprecated()
    return jsonify(signatures)

@signatures_bp.route("/api/signatures/test", methods=['GET'])
def get_test_signatures_view():
    signatures = get_test_signatures()
    return jsonify(signatures)

@signatures_bp.route("/api/signatures/isas/<apk_id>", methods=['GET'])
def get_apk_isas(apk_id):
    isas = get_isas(apk_id)
    return jsonify(isas)