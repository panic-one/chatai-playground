from flask import Blueprint

llm_bp = Blueprint("llm", __name__)

from . import llm_routes