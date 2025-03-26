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
            

class TextToParseService:

    nlp = spacy.load("fr_core_news_sm")

    @staticmethod
    def tokenize_and_conllize(text):
        
        text = TextToParseService.nlp(text)
        conll_string = ''

        for id_sent, sentence in enumerate(text.sents):
            sentence_text = sentence.text if '\n' not in sentence.text else sentence.text.replace("\n", "")

            index = 1
            conll_string += f"# sent_id = {id_sent}\n# text = {sentence_text}\n"
            for token in sentence:
                token_form = token.text.strip()  
                if token_form: 
                    conll_string += f"{index}\t{token_form}\t_\t_\t_\t_\t_\t_\t_\t_\t\n"
                    index += 1

            conll_string += '\n'

        return conll_string



