from flask import Flask 
from flask_restx import Api

from app.config import config_by_name
from app.routes import register_routes
from app.parser_config import ParserConfig

parser_config = ParserConfig()


def create_app(env):
    
    app_env = env
    app = Flask(__name__, instance_relative_config=False)
    parser_config.set_url(app_env)

    api = Api(
        app,
        title="BertForDeprel Quick parser",
        doc="/api/doc",
        endpoint="/api",
        base_url="/api"
    )

    register_routes(api, app)

    return app

    