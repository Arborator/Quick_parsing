import io 
import json
import zipfile

from flask_restx import Namespace, Resource
from flask import abort, request, send_file

from app.parser.service import ParserService, TextToParseService

api = Namespace("Parser", description="Endpoints dealing with the parser")


@api.route("/list")
class ParserModelsListResource(Resource):

    def get(self):

        response = ParserService.send_get_request('/list')
        print(response)
        if response['status'] == 'failure':
            error_message = f"Sorry the parser is unreachable, please contact the admins, {response['error']}"
            abort(503, error_message)

        else:
            models = response.get("data")
            models = ParserService.get_best_models(models)
            print(f"DEBUG: After filtering, returning {len(models)} models")
            return { "status": "success", "data": models }
        

@api.route("/start")
class ParserParseStartResource(Resource):

    def post(self):

      
        text_to_parse = request.form.get('text_to_parse')
        files = request.files.to_dict(flat=False).get("files")
    
        model = json.loads(request.form.get('model'))
        parsing_settings = json.loads(request.form.get('parsingSettings'))

        files_to_parse = {}
        
        if text_to_parse:
            text_conllized = TextToParseService.tokenize_and_conllize_with_kim(text_to_parse)
            files_to_parse['parsed_text'] = text_conllized

        if files: 
            for file in files:
                file_name = file.filename.split(".conllu")[0]
                files_to_parse[file_name] = file.read().decode()
       
        data = {
            "model_info": model["model_info"],
            "to_parse_samples": files_to_parse,
            "parsing_settings": parsing_settings
        }

        return ParserService.send_post_request("/parse/start", data)
    

@api.route("/status")
class ParserParseStatusResource(Resource):

    def post(self):

        params = request.get_json(force=True)
        parse_task_id = params["task_id"]

        data = { "parse_task_id": parse_task_id }
        parsing_status = ParserService.send_post_request("/parse/status", data)

        if parsing_status["status"] == "failure":

            return parsing_status
        
        data = parsing_status["data"]
        
        return  { "status": "success", "data": data }


        
