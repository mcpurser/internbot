from model.topline.powerpoint import qsf_topline_slides

import csv
import re
from collections import OrderedDict

class Powerpoint(object):

    def __init__(self):
        self.__frequencies = []

    def build_powerpoint_model(self, path_to_freqs, groups = [], survey = None):
        question_data = self.unicode_dict_reader(open(path_to_freqs))
        self.__survey = survey
        self.__groups = groups
        if self.__survey is not None:
            self.__questions = survey.get_questions()
            self.assign_frequencies(question_data)
        else:
            pass
        
    def unicode_dict_reader(self, utf8_data, **kwargs):
        csv_reader = csv.DictReader(utf8_data, **kwargs)
        for row in csv_reader:
            if row['variable'] != "":
                yield {key: value for key, value in row.items()}

    def assign_frequencies(self, question_data):
        for row in question_data:
            question_name = row["variable"]
            response_label = row["label"]
            question_stat = row["stat"]
            matching_question = self.find_question(question_name)
            if matching_question is not None:
                matching_response = self.find_response(row["value"], matching_question)
                if matching_response is not None:
                    self.add_frequency(matching_response, row)
                    self.add_n(matching_question, row)
                    self.add_stat(matching_question, question_stat)

    def build_powerpoint_report(self, path_to_template, path_to_output):
        if self.__survey is not None:
            report = qsf_topline_slides.QSFToplineSlides(self.__survey, path_to_template, path_to_output, self.__groups)
        else:
            pass
        report.save(str(path_to_output))

    def find_question(self, question_to_find):
        matching_question = self.__survey.blocks.find_question_by_name(question_to_find)
        if matching_question is None:
            print("\nCould not match question "+question_to_find+ " from CSV to a question in the QSF.\n             *This data will need to be input manually.*\n")
            return None
        elif matching_question.parent == "CompositeQuestion":
            matching_question = self.find_sub_question(matching_question, question_to_find)
        return matching_question

    def find_sub_question(self, composite_question, question_to_find):
        absolute_match = None
        for sub_question in composite_question.questions:
            if re.match(sub_question.name, question_to_find):
                absolute_match = sub_question
        return absolute_match

    def find_response(self, response_to_find, matching_question):
        if response_to_find == 'NA':
            matching_question.add_NA()
            return matching_question.get_NA()
        responses = matching_question.responses
        matching_response = next((response for response in responses if response.code == response_to_find), None)
        if response_to_find == 'On':
            matching_response = next((response for response in responses if response.response == '1'), None)

        if matching_response is None:
            matching_response = next((response for response in responses if response.response == response_to_find), None)
            if matching_response is None:
                print("\nCould not match response " +response_to_find+ " from " + matching_question.name + " from CSV to a question in the QSF.\n             *This data will need to be input manually.*\n")
        return matching_response

    def add_frequency(self, matching_response, frequency_data):
        self.__frequencies = OrderedDict()
        if len(self.__groups) > 0:
            for group in self.__groups:
                round_col = "result %s" % group
                if frequency_data[round_col] != "":
                    self.__frequencies[group] = float(frequency_data[round_col])
        else:
            round_col = "result"
            self.__frequencies[0] = float(frequency_data[round_col])
        matching_response.frequencies = self.__frequencies

    def add_n(self, matching_question, question_data):
        current_n = matching_question.n
        matching_question.n = current_n + int(question_data["n"])

    def add_display_logic(self, matching_question, question_display):
        matching_question.display_logic = question_display

    def add_stat(selfself, matching_question, stat):
        matching_question.stat = stat
