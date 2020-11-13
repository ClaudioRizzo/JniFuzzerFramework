'''This module is ment to enable the server to render our react application'''
from flask import Blueprint, send_from_directory, render_template

rendering_bp = Blueprint('rendering', __name__)


@rendering_bp.route('/')
def index():
    return render_template('index.html')

@rendering_bp.route('/<path:all>', methods=['GET'])
def render_react_app(all):
    return render_template('index.html')