from flask import Blueprint
import logging

from models import Strategy
from database import db_session, DBSession

strategy_api = Blueprint('strategy_api', __name__)
logger = logging.getLogger(__name__)

@strategy_api.route("", methods=["POST"])
def create_strategy(name, content, period, money):
    with DBSession() as session:
        new = Strategy(name=name,
                       content=content,
                       period=period,
                       money=money)
        session.add(new)



