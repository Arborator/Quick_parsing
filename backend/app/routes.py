def register_routes(api, app, root="api"):

    from app.parser import register_routes as attach_parser

    attach_parser(api, app, root)