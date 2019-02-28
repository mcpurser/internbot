from question import Question, Questions
from topline_report import ToplineReport
import csv

class ReportGenerator(object):
    def __init__(self, path_to_csv, round_no):
        self.__questions = Questions()
        self.read_csv(path_to_csv, round_no)

    def read_csv(self, path_to_csv, round_no):
        with open(path_to_csv, 'rb') as csvfile:
            file = csv.DictReader(csvfile, quotechar = '"')
            for question_data in file:
                self.__questions.add(question_data, round_no)

    def generate_basic_topline(self, path_to_template, path_to_output):
        report = ToplineReport(self.__questions, path_to_template)
        report.save(str(path_to_output) + '/trended_topline.docx')

