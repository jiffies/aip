from flask import Flask, jsonify
from database import db_session
from handlers.strategy import strategy_api
from handlers.plan import plan_api

app = Flask(__name__)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.errorhandler(404)
def page_not_found(error):
    return jsonify({"message": "404不存在"})

@app.errorhandler(500)
def exception(error):
    return jsonify({"message": "服务器错误"})

@app.route('/')
def hello_world():
    return '定投信息'

app.register_blueprint(strategy_api, url_prefix='/strategy')
app.register_blueprint(plan_api, url_prefix='/plan')


if __name__ == '__main__':

    app.run()
