from flask import Blueprint

threads_bp = Blueprint("threads", __name__, url_prefix="/threads")

from . import routes