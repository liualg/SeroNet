#!/usr/bin/env python
'''Generate Suggestions for the 
   JSON object from SeroNet Registry Excel Sheet
'''

import sys
import os
import glob
import json

import nltk
from nltk.corpus import stopwords

import ssl
try:
     _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
     pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
from nltk.tokenize import word_tokenize
nltk.download('punkt')

# from argparse import ArgumentParser

# if __name__ == "__main__":
#     parser = ArgumentParser(
#              prog="createSuggestions",
#              description="Add suggestions to SeroNet registry JSON")

#     parser.add_argument(
#         '--input_directory',
#         dest="input_directory",
#         required=True,
#         help="Specify the path to the input directory"
#     )

def add_NLKsuggestions(input_directory):
    print(input_directory)

    documents_in_directory = [ os.path.abspath(p) for p in glob.glob(input_directory + "/*.orig")]
    for document in documents_in_directory:
        (root, filename) = os.path.split(document)
        print(root, filename)
        with open(document, 'r') as f:
            suggestions_all = set()
            json_document = json.load(f)
            #print(json_document['study_name'])
            text_tokens = word_tokenize(json_document['study_name'])
            suggestions = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}

            text_tokens = word_tokenize(json_document['publication_title'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            text_tokens = word_tokenize(json_document['study_objective'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            text_tokens = word_tokenize(json_document['study_description'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            text_tokens = word_tokenize(json_document['primary_institution_name'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            text_tokens = word_tokenize(json_document['research_focus'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            text_tokens = word_tokenize(json_document['study_type'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            text_tokens = word_tokenize(json_document['clinical_study_design'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            for word in json_document['keyword']:
                suggestions.add(word.lower())

            for word in json_document['reported_health_condition']:
                suggestions.add(word.lower())

            for word in json_document['sars_cov_2_vaccine_type']:
                suggestions.add(word.lower())

            text_tokens = word_tokenize(json_document['clinical_outcome_measure'])
            s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
            suggestions.update(s1)            

            for obj in json_document['inclusion_exclusion']:
                text_tokens = word_tokenize(obj['inclusion_criterion'])
                s1 = {word.lower() for word in text_tokens if (not word.lower() in stop_words and len(word) > 2)}
                suggestions.update(s1)            

            suggestions_list = sorted(suggestions)

            filename = filename.replace(".orig", "")
            out_file_name = root + "/" + filename + ".orig"
            out_file = open(out_file_name, "w")
            json_document['suggestions'] = suggestions_list
            out_file.write(json.dumps(json_document, indent = 4))
            out_file.close()