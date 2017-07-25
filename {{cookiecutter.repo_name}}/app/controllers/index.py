from flask import Blueprint, render_template

from app.{{cookiecutter.repo_name}} import cache

index = Blueprint('index', __name__)

"""
Routes
"""


@index.route('/')
@cache.cached(timeout=1000)
def root():
    return render_template('index.html')
