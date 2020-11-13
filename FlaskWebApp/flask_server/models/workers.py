from flask import current_app
from bson.objectid import ObjectId
from flask_server.models.users import get_current_userid
import time


def push_job(user_id, apk_id, signature, timeout, isa):
    '''Inserts a job into the jobs collection.

    Params:
        (str) user_id: the user creating this job
        (str) apk_id: the id of the apk we are analysing
        (str) signature: the soot format signautre of the method to fuzz
        (int) timeout: how long we want to fuzz for
    '''
    data = {'apk_id': apk_id, 'signature': signature, 'timeout': timeout, 'isa': isa}
    job = {'progress': 0, 'user_id': user_id, 'status': 'available',
           'data': data, 'seen': False, 'utc_epoch_request': time.time(),
           'utc_epoch_completed': -1}
    _id = current_app.db.jobs.insert_one(job).inserted_id
    return str(_id)


def set_job_seen(job_id, seen):
    current_app.db.jobs.find_one_and_update({'_id': ObjectId(job_id)}, {'$set': {'seen': seen}})


def find_complted_jobs_by_users(user_id):
    '''Return a list of jobs started by the user with id `user_id` and complted.

    Param:
        (str) `user_id`: username of the user who started the job
    
    Return:
        (list) a list of completed jobs started by `user_id`
    '''
    jobs = current_app.db.jobs.find({'user_id': user_id, 'status': 'completed'})
    return [_strip_id(job) for job in jobs]


def find_jobs_by_users(user_id):
    '''Return a list of jobs started by the user with id `user_id`.

    Param:
        (str) `user_id`: username of the user who started the job
    
    Return:
        (list) a list of jobs started by `user_id`
    '''
    jobs = current_app.db.jobs.find({'user_id': user_id})

    return [_strip_id(job) for job in jobs]


def find_job_by_id(job_id):
    '''Return a job with the given `job_id`.
    None if no job has been found
    '''
    job = current_app.db.jobs.find_one({'_id': ObjectId(job_id)})
    if job is None or job['user_id'] != get_current_userid():
        return None
    return job


def _strip_id(job):
    '''given a job, it returns a sanitized version of it
    where the _id is a string version of ObjectId
    '''
    job['_id'] = str(job['_id'])
    return job

def find_completed_jobs_unseen_by(user_id):
    '''Return a list of jobs started by the user with id `user_id`,
    which are completed and unseen.

    Param:
        (str) `user_id`: username of the user who started the job
    
    Return:
        (list) a list of jobs started by `user_id`
    '''
    jobs = current_app.db.jobs.find({'user_id': user_id, 'seen': False, 'status': 'completed'})
    return [_strip_id(job) for job in jobs]


def find_jobs_started_by(user_id):
    '''Return a list of jobs started by `user_id`
    The list will be sorted by newer to older.
    '''
    jobs = current_app.db.jobs.find({'user_id': user_id})

    jobs = [_strip_id(job) for job in jobs]
    jobs.sort(key=lambda job: job['utc_epoch_request'], reverse=True)
    
    return jobs