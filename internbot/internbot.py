from model import model
from view import view

class Controller(object):

    def __init__(self):
        self.__view = view.View()
        self.__model = model.Model()

    @property
    def view(self):
        return self.__view

    def build_survey(self, path_to_qsf):
        return self.__model.survey(path_to_qsf)

    def build_appendix_model(self, path_to_csv):
        self.__model.build_appendix_model(path_to_csv)

    def build_appendix_report(self, path_to_output, is_spreadsheet, is_qualtrics):
        self.__model.build_appendix_report(path_to_output, 'resources/images/', 'resources/templates/appendix_template.docx', is_spreadsheet, is_qualtrics)

    def build_document_model(self, path_to_csv, groups, survey):
        self.__model.build_document_model(path_to_csv, groups, survey)

    def build_document_report(self, path_to_output):
        self.__model.build_document_report('resources/templates/topline_template.docx', path_to_output)

    def build_powerpoint_model(self, path_to_csv, groups, survey):
        self.__model.build_powerpoint_model(path_to_csv, groups, survey)

    def build_powerpoint_report(self, path_to_template, path_to_output):
        self.__model.build_powerpoint_report(path_to_template, path_to_output)

    def build_scores_model(self, path_to_csv, round, location):
        self.__model.build_scores_model(path_to_csv, round, location)

    def build_scores_report(self, path_to_output):
        self.__model.build_scores_report(path_to_output)

    def build_issues_model(self, path_to_csv, round):
        self.__model.build_issues_model(path_to_csv, round)

    def build_issues_report(self, path_to_output):
        self.__model.build_issues_report(path_to_output)

    def build_trended_model(self, path_to_csv, round):
        self.__model.build_trended_model(path_to_csv, round)

    def build_trended_report(self, path_to_output):
        self.__model.build_trended_report(path_to_output)

if __name__ == '__main__':
    controller = Controller()
    controller.view.controller = controller
    controller.view.run()