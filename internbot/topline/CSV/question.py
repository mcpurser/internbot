from collections import OrderedDict


class Questions(object):

    def __init__(self, questions_data=[]):
        self.__questions = OrderedDict()
        for question_data in questions_data:
            self.add(question_data)

    def add(self, question_data, round_no):
        display_logic = question_data['logic']
        question_name = question_data['variable']
        question_prompt = question_data['prompt']
        question_response = question_data['label']
        question_pop = question_data['n']
        if self.already_exists(question_name):
            question = self.get(question_name)
            if question_response != "":
                question.add_response(question_response, question_data, round_no)
            if display_logic != "":
                question.add_display(display_logic)
        else:
            question = Question(question_name, question_prompt, question_pop)
            if question_response != "":
                question.add_response(question_response, question_data, round_no)
            if display_logic != "":
                question.add_display(display_logic)
            self.__questions[question.name] = question

    def get(self, question_name):
        return self.__questions.get(question_name)

    def already_exists(self, question_name):
        if self.get(question_name) is None:
            return False
        else:
            return True

    def __len__(self):
        return len(self.__questions)

    def list_names(self):
        result = self.__questions.keys()
        return result

    def __repr__(self):
        result = ''
        for name, question in self.__questions.iteritems():
            result += str(question)
            result += '\n'
        return result


class Question(object):

    def __init__(self, name, prompt, n):
        self.__name = name
        self.__prompt = prompt
        self.__n = n
        self.__responses = []
        self.__display_logic = ""

    @property
    def name(self):
        return self.__name

    @property
    def prompt(self):
        return self.__prompt

    @property
    def n(self):
        return self.__n

    @property
    def responses(self):
        return self.__responses

    @property
    def display_logic(self):
        return self.__display_logic

    def add_response(self, response_name, response_data, round_no):
        self.__responses.append(Response(response_name, response_data, round_no))

    def add_display(self, logic):
        self.__display_logic = logic


class Response(object):

    def __init__(self, label, frequency_data, round_no):
        self.__name = label
        self.__frequencies = []
        round_col = "percent" 
        if frequency_data.get(round_col) is not None:
            self.__frequencies.append(frequency_data[round_col])
        else:
        	iteration = 1
        	round_int = int(round_no)
        	while iteration <= round_int:
        		round_col = "percent %s" % iteration
        		if frequency_data[round_col] != '':
        			self.__frequencies.append(frequency_data[round_col])
        		iteration += 1

    @property
    def name(self):
        return self.__name

    @property
    def frequencies(self):
        return self.__frequencies
