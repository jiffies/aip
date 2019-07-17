from flask import Blueprint, jsonify, request, abort
from service.feixiaohao import get_currency_price

import logging

from sqlalchemy.orm.attributes import flag_modified

from models import Plan, Record
from database import db_session, DBSession

plan_api = Blueprint('plan_api', __name__)
logger = logging.getLogger(__name__)

@plan_api.route("", methods=["POST"])
def create_plan():
    with DBSession() as session:
        new = Plan(name=request.get_json().get("name"),
                   content={})
        session.add(new)
    db_session().refresh(new)
    return jsonify({k: v for k,v in new.__dict__.items() if k in new._sa_instance_state.attrs.keys()})

@plan_api.route("/record", methods=["POST"])
def add_record():
    content = request.get_json().get("content")

    with DBSession() as session:
        plan = db_session().query(Plan).filter(
            Plan.id == request.get_json().get("plan_id")).one()
        if not plan:
            abort(404)

        for currency, detail in content.items():
            if currency not in plan.content:
                plan.content[currency] = {}
                plan.content[currency]["total_amount"] = 0
                plan.content[currency]["total_quantity"] = 0
                plan.content[currency]["avg_price"] = 0
                plan.content[currency]["ratio"] = 0
            plan.content[currency]["total_amount"] += detail["amount"]
            plan.content[currency]["total_quantity"] += detail["quantity"]
            plan.content[currency]["avg_price"] = plan.content[currency]["total_amount"] / plan.content[currency]["total_quantity"]
            plan.content[currency]["earning"] = (float(get_currency_price().get(currency)) - plan.content[currency]["avg_price"]) / plan.content[currency]["avg_price"]
            plan.total_invest_money += detail["amount"]
        for currency, detail in plan.content.items():
            plan.content[currency]["ratio"] = plan.content[currency]["total_amount"] / plan.total_invest_money

        new = Record(plan_id=request.get_json().get("plan_id"),
                     content=content)
        session.add(new)
        flag_modified(plan, "content")

    db_session().refresh(plan)
    total = 0
    for currency, detail in plan.content.items():
        total += float(get_currency_price().get(currency)) * detail.get("total_quantity")
    total_earning = (total - plan.total_invest_money) / plan.total_invest_money
    result = {k: v for k, v in plan.__dict__.items() if
     k in plan._sa_instance_state.attrs.keys()}
    result["total_earning"] = total_earning
    return jsonify(result)



