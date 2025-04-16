import requests
import json
import spacy

from app import parser_config

class ParserService:

    @staticmethod
    def send_get_request(url_suffix):

        url = f"{parser_config.server}/parser/models{url_suffix}"
        try:
            response = requests.get(url)
            return response.json()
        except requests.exceptions.ReadTimeout:
            error_message = f"connection timout with `url={url}`"
            return {"status": "failure", "error": error_message }
        except Exception as e:
            error_message = f"unknown error when connecting `url={url}` : {str(e)}"
            return {"status": "failure", "error": error_message}
        
    
    @staticmethod
    def send_post_request(url_suffix, data):

        url = f"{parser_config.server}/parser/models{url_suffix}"
        try:
            response = requests.post(url, json=data)
            data = response.json()
            if data.get("schema_errors"):
                return {
                    "status": "failure",
                    "error": f"You have a problem with at least one of the sentence "
                             f"you sent : {json.dumps(data.get('schema_errors'))}",
                    "schema_errors": data.get("schema_errors"),
                }
            return data
        except requests.exceptions.ReadTimeout:
            error_message = f"<ArboratorParserAPI> connection timout with `url={url}`"
            return {"status": "failure", "error": error_message }
        except Exception as e:
            error_message = f"<ArboratorParserAPI> unknown error when connecting `url={url}` : {str(e)}"
            return {"status": "failure", "error": error_message}

    @staticmethod
    def get_best_models(available_models):
        best_models_dict = {}

        for model in available_models:
            project_name = model["model_info"]["project_name"]
            best_las = model["scores_best"]["LAS_epoch"]

            if project_name not in best_models_dict or best_las > best_models_dict[project_name]["scores_best"]["LAS_epoch"]:
                best_models_dict[project_name] = model

        best_models = list(best_models_dict.values())
        return best_models


from spacy.language import Language
from spacy.tokens import Doc

class TextToParseService:

    nlp = spacy.load("fr_core_news_sm")

    @Language.component("custom_sentencizer")
    def custom_sentencizer(doc: Doc) -> Doc:
        for token in doc[:-1]:
            if token.text in [".", "!", "?"]:
                doc[token.i + 1].is_sent_start = True
        return doc

    
    nlp.remove_pipe("parser")  
    nlp.add_pipe("custom_sentencizer", before="ner")

    @staticmethod
    def tokenize_and_conllize(text):
        text = text.replace("\n", " ")
        text = TextToParseService.nlp(text)
        
        conll_string = ''

        for id_sent, sentence in enumerate(text.sents):
            sentence_text = sentence.text.strip() 
            conll_string += f"# sent_id = {id_sent}\n# text = {sentence_text}\n"
            for index, token in enumerate(sentence, 1):
                token_form = token.text.strip()
                if token_form:
                    conll_string += f"{index}\t{token_form}\t_\t_\t_\t_\t_\t_\t_\t_\n"
            conll_string += '\n'
        return conll_string


