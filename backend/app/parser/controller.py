import io 
import zipfile

from flask_restx import Namespace, Resource
from flask import abort, request, send_file

from app.parser.service import ParserService, TextToParseService

api = Namespace("Parser", description="Endpoints dealing with the parser")


@api.route("/list")
class ParserModelsListResource(Resource):

    def get(self):

        response = ParserService.send_get_request('/list')

        if response['status'] == 'failure':
            error_message = f"Sorry the parser is unreachable, please contact the admins, {response['error']}"
            abort(503, error_message)

        else:
            models = response.get("data")
            return { "status": "success", "models": models }
        

@api.route("/start")
class ParserParseStartResource(Resource):

    def post(self):
        
        text_to_parse = request.form.get('text_to_parse')
        files = request.files.to_dict(flat=False).get("files")
        model = request.form.get('model')

        files_to_parse = {}
        
        if text_to_parse:
            text_conllized = TextToParseService.tokenize_and_conllize(text_to_parse)
            print(text_conllized)
            files_to_parse['parsed_text'] = text_conllized

        if files: 
            for file in files:
                files_to_parse[file.filename] = file.read()

        data = {
            "model_info": model,
            "to_parse_samples": files_to_parse
        }

        #return ParserService.send_post_request("/parse/start", data)
    

@api.route("/status")
class ParserParseStatusResource(Resource):

    def post(self):

        params = request.get_json(force=True)
        parse_task_id = params["task_id"]

        data = { "parse_task_id": parse_task_id }
        parsing_status = ParserService.send_post_request("parser/status", data)

        if parsing_status["status"] == "failure":

            return parsing_status
        
        data = parsing_status["data"]
        if data.get("ready") and data.get("parsed_samples"):

            task_parsed_samples = data["parsed_samples"]
            zip_buffer = io.BytesIO()

            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        
                for file_name, file_content in task_parsed_samples.items():
                    zip_file.writestr(f"{file_name}.conllu", file_content)

            zip_buffer.seek(0)

        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='files.zip'
        )







        


        
        



            







        