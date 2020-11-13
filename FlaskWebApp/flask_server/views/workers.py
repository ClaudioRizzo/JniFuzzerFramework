# -*- coding: utf-8 -*-

"""
flask_server.views.apks
~~~~~~~~~~~~~~~~~~~~

API routes for creating a job for the workers.

"""
from flask import Blueprint, jsonify, current_app, send_file, request
from flask_server.models.users import get_current_userid, is_logged_in
from flask_server.models.workers import (push_job,
                                      find_completed_jobs_unseen_by, 
                                      find_complted_jobs_by_users, 
                                      set_job_seen,
                                      find_job_by_id,
                                      find_jobs_started_by)
from flask_server.models.users import get_current_userid
import flask_server.models.apks as apk_model

import os


workers_bp = Blueprint('workers', __name__)


@workers_bp.route('/api/workers/unseen-jobs', methods=['GET'])
@is_logged_in
def find_unseen_complted_jobs_by_user():
    data = {'jobs': [], 'success': False}
    user_id = get_current_userid()
    if user_id is '':
        return jsonify(data)
    
    data['jobs'] = find_completed_jobs_unseen_by(user_id)
    return jsonify(data)

@workers_bp.route('/api/workers/completed-jobs', methods=['GET'])
@is_logged_in
def find_completed_jobs():
    data = {'jobs': [], 'success': False}
    user_id = get_current_userid()
    
    if user_id is '':
        return jsonify(data)
    
    data['jobs'] = find_complted_jobs_by_users(user_id)
    return jsonify(data)


@workers_bp.route('/api/workers/completed-jobs/', methods=['POST'])
@is_logged_in
def set_job_seen_value():
    job_id = request.get_json().get('job_id')
    seen = request.get_json().get('seen')
    set_job_seen(job_id, seen)
    
    data = {'jobs': [], 'success': False}
    user_id = get_current_userid()
    data['jobs'] = find_complted_jobs_by_users(user_id)
    return jsonify(data)

@workers_bp.route('/api/worker/jobs/<job_id>/download', methods=['GET'])
@is_logged_in
def download_job(job_id):
    job = find_job_by_id(job_id)
    
    result_id = job['result_id']
    apk_id = job['data']['apk_id']
    
    result_path = os.path.join(current_app.config['DOWNLOAD_RESULT_FOLDER'], apk_id, result_id, 'workspace.zip')

    return send_file(result_path, as_attachment=True)

@is_logged_in
def push_job_to_worker(user_id, apk_id, signature, timeout, isa, token=""):
    return push_job(user_id, apk_id, signature, timeout, isa)
    
    


@workers_bp.route('/api/workers/push-job', methods=['POST'])
def create_job_for_worker():
    '''Pushes a job in to the db. The job will be
    performed by one of our running workers.
    `token` is used by @is_logged_in wrapper to 
    enable token authentications.

    From the client we expect a json containing:
        apk_id: the id of the apk under analysis
        signature: the signature to fuzz
        timout: timeout in seconds for the length of the fuzzing
        isa: isa of the library we extract the method from
    '''
    
    success = {'success': True}
    failure = {'success': False, 'msg': ''}

    # [0.5h, 1h, 3h, 6h, 12h, 24h, 48h]
    supported_timeouts = [60, 30*60, 60*60, 60*60*3,
                          60*60*6, 60*60*12,
                          60*60*24, 60*60*48]  # values are in seconds

    supported_isas = ['armeabi', 'armeabi-v7a', 'x86_64', 'x86']

    apk_id = request.get_json().get('apk_id')
    signature = request.get_json().get('signature')
    timeout = request.get_json().get('timeout')
    isa = request.get_json().get('isa')
    token = request.get_json().get('token')
    
    if timeout not in supported_timeouts:
        # we should return a failure and abort
        failure['msg'] = "Timeout not supported: {}".format(timeout)
        return jsonify(failure)

    if isa not in supported_isas:
        failure['msg'] = "isa not supported"
        return jsonify(failure)

    if apk_model.find_apk(apk_id) is None and apk_id != "test":
        failure['msg'] = "Apk not found"
        return jsonify(failure)

    if signature is "" or signature is None:
        failure['msg'] = "invalid signature"
        return jsonify(failure)

    user_id = get_current_userid(token=token)
    if user_id is "":
        failure['msg'] = "token"
        return jsonify(failure)
    
    job = push_job_to_worker(user_id, apk_id, signature, timeout, isa, token=token)

    success['job_id'] = job
    return jsonify(success) 

@workers_bp.route('/api/workers/active-jobs', methods=['GET'])
@is_logged_in
def get_active_jobs_for_user():
    user_id = get_current_userid()
    jobs = find_jobs_started_by(user_id)
    return jsonify(jobs)

@workers_bp.route('/api/workers/job-progress/<job_id>', methods=['GET'])
@is_logged_in
def get_job_progress(job_id):
    failure = {'success': False}
    job = find_job_by_id(job_id)
    
    if job is None or job['user_id'] != get_current_userid():
        return jsonify(failure)
    
    return jsonify({'progress': job['progress'], 'status': job['status']})
