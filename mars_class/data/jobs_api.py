import flask
from flask import jsonify, make_response, request
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

from . import db_session
from .db_session import SqlAlchemyBase
from .jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs': [item.to_dict(only=(
                'team_leader', 'job', 'work_size', 'collaborators', 'is_finished')) for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_job(news_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(news_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'jobs': jobs.to_dict(only=(
                'team_leader', 'job', 'work_size', 'collaborators', 'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators', 'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(news_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(news_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def update_jobs(jobs_id):
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size', 'collaborators',
                  'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    db_sess.query(Jobs).filter(Jobs.id == jobs_id). \
        update({'team_leader': request.json['team_leader'],
                'job': request.json['job'],
                'work_size': request.json['work_size'],
                'collaborators': request.json['collaborators'],
                'is_finished': request.json['is_finished']})
    db_sess.commit()
    return jsonify({'id': jobs_id})
