from flask import Blueprint, redirect, abort

bp_web = Blueprint('main', __name__, url_prefix='')

@bp_web.route('/', methods=['GET'])
def index():
    # abort(404)
    return redirect("/api/doc/")
        