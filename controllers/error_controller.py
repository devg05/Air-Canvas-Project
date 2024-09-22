# error_handlers.py
from flask import Blueprint
import traceback

# Create a Blueprint for error handlers
error_handlers = Blueprint('error_handlers', __name__)

@error_handlers.app_errorhandler(500)
def internal_error(error):
    print(traceback.format_exc())  # Print the full error traceback
    return "An internal error occurred.", 500

@error_handlers.app_errorhandler(404)
def page_not_found(error):
    return "Page not found", 404
