import langdetect
import json
import nltk
import argparse
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')


class NeologismChecker:
    def __init__(self, term, year, lang=None, mapping=None, survey_response=None):
        self.term = term
        self.year = year
        self.lang = lang
        self.mapping = mapping
        self.survey_response = survey_response
    
    def filter_year(self):
        return 2015 <= int(self.year) <= 2025 if self.year is not None else False
    
    def drop_null(self):
        return self.term is not None and self.year is not None
    
    def detect_language(self):
        try:
            detected_lang = langdetect.detect(self.term)
            return detected_lang == self.lang
        except langdetect.lang_detect_exception.LangDetectException:
            return False
    
    def remove_ppn(self):
        if self.term is None:
            return False
        words = word_tokenize(self.term)
        tagged_term = pos_tag(words)
        propernouns = [word for word, pos in tagged_term if pos == 'NNP']
        return len(propernouns) == 0
    
    def filter_mapping(self):
        return self.mapping is not None
    
    def filter_survey_response(self):
        return self.survey_response is not None and int(self.survey_response) >= 3
    
    def is_neologism(self):
        checks = {
            "filter_year": self.filter_year(),
            "drop_null": self.drop_null(),
            "detect_language": self.detect_language(),
            "remove_ppn": self.remove_ppn(),
            "filter_mapping": self.filter_mapping(),
            "filter_survey_response": self.filter_survey_response()
        }
        fail_types = [key for key, value in checks.items() if not value]
        return all(checks.values()), fail_types


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", type=str, default='test.jsonl')
    parser.add_argument("--output_file", type=str, default='test_new.jsonl')
    args = parser.parse_args()

    with open(args.input_file, 'r', encoding='utf-8') as infile, \
        open(args.output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            data = json.loads(line)
            src_lang = data.get("src_lang")
            tgt_lang = data.get("tgt_lang")
            
            checker = NeologismChecker(
                term=data.get(f"{src_lang}_neologism"),
                year=data.get("year"),
                lang=data.get("src_lang"),
                mapping=data.get(f"{tgt_lang}_mapping"),
                survey_response=data.get("survey_frequency")
            )
            is_neologism, fail_types = checker.is_neologism()
            data["is_neologism"] = is_neologism
            data["fail_type"] = fail_types if not is_neologism else []
            outfile.write(json.dumps(data, ensure_ascii=False) + "\n")
