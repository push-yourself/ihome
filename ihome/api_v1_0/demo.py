
from . import api
from flask import current_app
from ihome import models,db
import logging
@api.route("/index")
def index():
    current_app.logger.error('error msg')
    return 'index page'