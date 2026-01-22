import requests
import json
import spacy
import os

from app import parser_config

class ParserService:

    @staticmethod
    def send_get_request(url_suffix):

        url = f"{parser_config.server}/parser/models{url_suffix}"
        headers = {
            "X-Application-Models": "quick_parser",
        }
        try:
            response = requests.get(url, headers=headers)
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
    
    @staticmethod
    def tokenize_and_conllize_with_kim(text):

       
        sent2toks = tokenize_plain_text(text, lang='fr')
        conll_string = conllize_plain_text(sent2toks, sample_name="sample", start=0)
        
        return conll_string


###########################"tokenizer Kim's script" ###########################
"""We used the tokenizer of Kim https://github.com/kimgerdes/text2conll instead of the one in spacy"""
import re



re_url = re.compile(r'''(https?://|\w+@)?[\w\d\%\.]*\w\w\.\w\w[\w\d~/\%\#]*(\?[\w\d~/\%\#]+)*''', re.U+re.M+re.I)
# combinations of numbers:
re_spacenum = re.compile(r'\d+[ ,.]+[0-9 ,.]*\d+')
# regex to match escapes \number\ used for special words:
rerematch = re.compile(r'\\\d+\\')

def tokenize_plain_text( text,
              lang,
              sent_ends='.;!?\\n',
              new_sent_upper='.!?',
              char_in_word='_-',
              whole_words="aujourd'hui l'on etc. Mr. M. Nr. N° ;) ;-)",
              special_suffix="n't -je -tu -il -elle -on -nous -vous -ils -ils -elles -y -t-il -t-elle -t-ils -t-ils -t-on",
              keep_url=True, 
              combine_numbers=True, 
              sent_cut="", 
              escape = '____',
              sent_not_cut="§§§",
             ):
     """
	text: 
		Text a transformer en Conll
	sent_ends='.;!?\\n'
		These characters end a sentence backslach escapes should be double escaped like \\n
	new_sent_upper=".!?"
		If not empty, these characters end a sentence only if the following character is upper case, should be a subset of sent_ends
	char_in_word='_-', 
		Characters that should be treated as letters inside words
	glue_left="'~", 
		Cut token after these characters 
	glue_right="" 
		Cut token before these characters 
	whole_words="aujourd'hui l'on etc. Mr. M. Nr. N° ;) ;-)", 
		Keep these space-separated words as one tokens
	special_suffix="n't -je -tu -il -elle -on -nous -vous -ils -ils -elles -y -t-il -t-elle -t-ils -t-ils -t-on",
		Keep these space-separated suffixes as separate tokens
	keep_url=True, 
		Look for URLs and keep them together
	combine_numbers=True, 
		Spaces, commas, and points between numbers are grouped together such as 999 349
	sent_cut="", 
	 	A unique word or sequence where cutting should be done. if set, sent_ends is ignored
	escape = '____', 
		No need to change this. should be letters (\w) used to escape internally. 
		Should not appear anywhere in the text
	sent_not_cut="§§§", # symbols that have been placed after the potential sent_ends that should not end the sentence. 
		This should be a unique symbol not appearing anywhere naturally in the text as it will be removed from the text.
		for example use sent_not_cut="§§§"
	"""
     whole_words = whole_words.strip().split()
     special_suffix = special_suffix.strip()
     num_dot = (escape+'{}'+escape).format('NUMBERDOT')
     space_after_esc = (escape+'{}'+escape).format('NOSPACEAFTER')
     if lang == 'fr':
        glue_left="'~"
        glue_right=""
     else:
        glue_left=""
        glue_right="'"
     ind = 0
     ntext = text
     for word in whole_words: 
        ntext = ntext.replace(word,'\\{ind}\\'.format(ind=ind))
        ind +=1
     if special_suffix:
        respecial_suffix = re.compile(r'({})\b'.format('|'.join(special_suffix.split())))
        for m in respecial_suffix.finditer(ntext):
             ntext = ntext.replace(m.group(0),'\\{ind}\\'.format(ind=ind))
             whole_words += [m.group(0)]
             ind +=1
     if keep_url:
        for murl in re_url.finditer(ntext):
            ntext = ntext.replace(murl.group(0),'\\{ind}\\'.format(ind=ind))
            whole_words += [murl.group(0)]
            ind +=1
     if combine_numbers:
        for mnum in re_spacenum.finditer(ntext):
            ntext = ntext.replace(mnum.group(0),'\\{ind}\\'.format(ind=ind))
            whole_words += [mnum.group(0)]
            ind +=1

	# replace "the 2. guy" by "the 2___NUMDOT___ guy":
     re_num_dot = re.compile(r'\b(\d+)\.(?! [0-9A-ZÀÈÌÒÙÁÉÍÓÚÝÂÊÎÔÛÄËÏÖÜÃÑÕÆÅÐÇØ])') # num followed by . not followed by upper case
     ntext = re_num_dot.sub(r'\1'+num_dot, ntext)
	# now we split into sentences:
     if sent_cut: 
        sents = ntext.split(sent_cut)
     else:
        if new_sent_upper:
            sent_ends_nopoint = re.sub(r'[{new_sent_upper}]+'.format(new_sent_upper=new_sent_upper),'', sent_ends)
            if sent_not_cut:
                re_sent_bounds = re.compile(
					'(([{sent_ends_nopoint}]+(?!{sent_not_cut})\s*)|([{sent_ends}]+(?!{sent_not_cut})\s*(?=[0-9\\\A-ZÀÈÌÒÙÁÉÍÓÚÝÂÊÎÔÛÄËÏÖÜÃÑÕÆÅÐÇØ])))'.format(
								sent_ends_nopoint=sent_ends_nopoint, 
								sent_ends=new_sent_upper.replace('.','\.'),
								sent_not_cut=sent_not_cut), re.U+re.M)
            else:
                re_sent_bounds = re.compile(
					'(([{sent_ends_nopoint}]+\s*)|([{sent_ends}]+\s*(?=[0-9\\\A-ZÀÈÌÒÙÁÉÍÓÚÝÂÊÎÔÛÄËÏÖÜÃÑÕÆÅÐÇØ])))'.format(
								sent_ends_nopoint=sent_ends_nopoint, 
								sent_ends=new_sent_upper.replace('.','\.'),
								sent_not_cut=sent_not_cut), re.U+re.M)
        else:
            if sent_not_cut:
                re_sent_bounds = re.compile(
					'([{sent_ends}](?!{sent_not_cut})+\s*)'.format(sent_ends=sent_ends, 
						    sent_not_cut=sent_not_cut), re.U+re.M)
            else:
                re_sent_bounds = re.compile(
					'([{sent_ends}]+\s*)'.format(sent_ends=sent_ends), re.U+re.M)
        doubsents = re_sent_bounds.split(ntext)+['']
        sents = []
        for i in range(0, len(doubsents), 2):
            if doubsents[i] and doubsents[i+1] is not None:
                sents += [(doubsents[i].replace(sent_not_cut,'') + (doubsents[i+1] if i+1 < len(doubsents) else '')).strip()]
	
	### now we got the sents list, making the actual tokens
     retok = re.compile("(?!(\\\\d+\\\)|([\\\{} ]+))(\W+)(?!\d)".format(re.escape((char_in_word+glue_left+glue_right).replace('-','\-'))))
     reglue_left = re.compile(r'([{}])'.format(glue_left)) if glue_left else None
     reglue_right = re.compile(r'([{}])'.format(glue_right)) if glue_right else None
     stoks = {}
     def simplerematchreplace(matchobj): # used to reconstruct the sentence
        return whole_words[int(matchobj.group(0)[1:-1])]
     def rematchreplace(matchobj): # used to build the correct tokens
        if special_suffix and respecial_suffix.match(whole_words[int(matchobj.group(0)[1:-1])]):
            return space_after_esc+whole_words[int(matchobj.group(0)[1:-1])]
        return whole_words[int(matchobj.group(0)[1:-1])]
     for si,s in enumerate(sents):
        rs = rerematch.sub(simplerematchreplace,s.replace(num_dot,'.'))
        if glue_left: s = reglue_left.sub(r'\1 ', s)
        if glue_right: s = reglue_right.sub(r' \1', s)
        s = retok.sub(r'{}\3 '.format(space_after_esc), s) # adding the additional spaces
        toks = []
        spaceafters = []
        for t in s.split():
            t = t.replace(num_dot,'.')
            ts = rerematch.sub(rematchreplace,t) if rerematch.search(t) else t
            tsl = [tt for tt in ts.split(space_after_esc) if tt] 
            toks+= tsl
            spaceafters += [ii==len(tsl)-1 for ii,tt in enumerate(tsl)]
        stoks[(si,rs)] = list(zip(toks,spaceafters)) # 'si' makes keys unique and allows duplicate sentences
     return stoks

def conllize_plain_text(sent2toks, sample_name, start):
    conlls=[]
    for (si,s),toksas in sent2toks.items():
        conllines=[
            '# sent_id = {id}__{ind}'.format(id=sample_name,ind=start+1),
            '# text = {s}'.format(s=s)
        ]
        for i,(tok,sa) in enumerate(toksas):
            li = '{ind}\t{tok}\t_\t_\t_\t_\t_\t_\t_\t{spac}\t'.format(ind=i+1,tok=tok,spac='_' if sa else 'SpaceAfter=No')
            conllines+=[li]
        conlls+=['\n'.join(conllines)]
        start+=1
    return '\n\n'.join(conlls)+'\n'
