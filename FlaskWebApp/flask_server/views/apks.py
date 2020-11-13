# -*- coding: utf-8 -*-

"""
flask_server.views.apks
~~~~~~~~~~~~~~~~~~~~

API routes for querying and modifying the apk details of the dataset. 

"""
import os

from flask import Blueprint, jsonify, current_app, send_file, request

import flask_server.utils as utils
from flask_server.models import users, apks

apks_bp = Blueprint('apks', __name__)


@apks_bp.route("/api/apks", methods=['GET'])
@users.is_logged_in
def find_apks_ids_with_flow():
    if request.method == 'GET':
        return jsonify(apks.list_apks_with_flows())
    

@apks_bp.route("/api/apks", methods=['POST'])
@users.is_logged_in
def find_apks():
    if request.method == 'POST':
        apk_ids = request.get_json().get('apks')
        return jsonify(apks.find_apk_list(apk_ids))


@apks_bp.route("/api/apks/search/<partial_id>", methods=['GET'])
@users.is_logged_in
def find_apks_starting_with(partial_id):
    apk_ids = apks.find_apks_starts_with(partial_id)
    return jsonify(apk_ids)


@apks_bp.route("/api/apks/summaries", methods=['GET'])
@users.is_logged_in
def find_apk_summaries_with_flow():
    return jsonify(apks.list_apk_summaries_with_flows())


@apks_bp.route("/api/apks/<apk_id>", methods=['GET'])
@users.is_logged_in
def find_apk(apk_id):
    return jsonify(apks.find_apk(apk_id))


@apks_bp.route("/api/apks/<apk_id>/tags", methods=['GET'])
@users.is_logged_in
def find_apks_tags(apk_id):
    return jsonify(apks.find_apk(apk_id)['tags'])


@apks_bp.route("/api/tags", methods=['GET'])
@users.is_logged_in
def find_standard_tags():
    return jsonify(apks.get_standard_tags())


@apks_bp.route("/api/apks/<apk_id>/tags/<tag>/set", methods=['GET', 'POST'])
@users.is_logged_in
def set_apk_tag(apk_id, tag):
    apks.set_tag(apk_id, tag, True)
    return jsonify({'success': True})


@apks_bp.route("/api/apks/<apk_id>/tags/<tag>/unset", methods=['GET', 'POST'])
@users.is_logged_in
def unset_apk_tag(apk_id, tag):
    apks.set_tag(apk_id, tag, False)
    return jsonify({'success': True})


@apks_bp.route("/api/apks/<apk_id>/download", methods=['GET'])
@users.is_logged_in
def download_apk(apk_id):
    filepath = os.path.join(
        current_app.config['DOWNLOAD_FOLDER'], *apk_id[:3], apk_id + '.apk')
    print(filepath)
    return send_file(filepath, as_attachment=True)


@apks_bp.route("/api/apks/<apk_id>/notes/add", methods=['POST'])
@users.is_logged_in
def add_note(apk_id):
    apk = apks.find_apk(apk_id)

    if apk is None:
        return utils.error('apk {} not found'.format(apk_id))

    title = request.get_json().get('title')
    text = request.get_json().get('text')

    note = apks.add_note(title, text, apk_id)
    note['_id'] = str(note['_id'])
    # The front-end needs the note_id to simplify the delete functionality
    return jsonify(note)


@apks_bp.route("/api/notes/<note_id>/delete", methods=['POST'])
@users.is_logged_in
def delete_note(note_id):
    note = apks.find_note(note_id)

    if note is None:
        return utils.error('note {} not found'.format(note_id))

    apks.delete_note(note_id)
    return jsonify({'success': True})


@apks_bp.route("/api/apks/<apk_id>/libs", methods=['GET'])
@users.is_logged_in
def find_libs_by_apk(apk_id):
    libs = apks.find_libs_by_apk(apk_id)
    if libs is None:
        return utils.error('apk {} not found'.format(apk_id))
    return jsonify(libs)


@apks_bp.route("/api/apks/<apk_id>/flows", methods=['GET'])
@users.is_logged_in
def find_flows_by_apk(apk_id):
    flows = apks.find_flows_by_apk(apk_id)
    if flows is None:
        return utils.error('apk {} not found'.format(apk_id))
    return jsonify(flows)


@apks_bp.route("/api/apks/<apk_id>/notes", methods=['GET'])
@users.is_logged_in
def find_notes_by_apk(apk_id):
    notes = apks.find_notes_by_apk(apk_id)
    if notes is None:
        return utils.error('apk {} not found'.format(apk_id))
    return jsonify(notes)
