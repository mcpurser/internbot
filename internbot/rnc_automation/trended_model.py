from collections import OrderedDict

class TrendedModels(object):

    def __init__(self, models_data = []):
        self.__models = OrderedDict()
        for model_data in models_data:
            self.add(model_data)

    def add(self, model_data):
        if self.already_exists(model_data['Model']):
            model = self.get(model_data['Model'])
            model.add_field(model_data['Field Name'], model_data['Grouping'], model_data['Count'], model_data['Percent'])
        else:
            self.add_new(model_data)

    def add_new(self, model_data):
        new_model = Model(model_data['Model'])
        new_model.add_field(model_data['Field Name'], model_data['Grouping'], model_data['Count'], model_data['Percent'])
        self.__models[new_model.name] = new_model

    def get(self, model_name):
        return self.__models.get(model_name)

    def already_exists(self, model_name):
        if self.get(model_name) is None:
            return False
        else:
            return True

    def __iter__(self):
        return iter(self.__models)

    def __len__(self):
        return len(self.__models)

    def __repr__(self):
        result = ''
        for name, model in self.__models.iteritems():
            result += str(model)
            result += '\n'
        return result

    def list_names(self):
        result = self.__models.keys()
        return result

    def get_fields(self, model_name):
        result = self.__models.get(model_name)
        return result.list_names()

    def model(self, model_name):
        return self.__models.get(model_name)

class Model(object):

    def __init__(self, name):
        self.name = name
        self.fields = OrderedDict()

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = str(name)

    def add_field(self, field, grouping, count, percent):
        if self.already_exists(field):
            add_field = self.get(field)
            add_field.add_grouping(grouping, count, percent)
        else:
            self.add_new(field, grouping, count, percent)

    def add_new(self, field, grouping, count, percent):
        new_field = Field(field)
        new_field.add_grouping(grouping, count, percent)
        self.fields[new_field.get_name()] = new_field

    def get(self, field_name):
        return self.fields.get(field_name)

    def already_exists(self, field_name):
        if self.get(field_name) is None:
            return False
        else:
            return True

    def __iter__(self):
        return iter(self.fields)

    def __len__(self):
        return len(self.fields)

    def __repr__(self):
        result = ''
        for name, field in self.fields.iteritems():
            result += str(field)
            result += '\n'
        return result

    def list_names(self):
        result = self.fields.keys()
        return result

    @property
    def return_variable(self):
        return self.variables

    def get_weighted_freq(self, variable):
        result = self.variables[variable].weighted_frequency

    def get_unweighted_freq(self, variable):
        result = self.variables[variable].unweighted_frequency

class Field(object):

    def __init__(self, name):
        self.name = name
        self.groupings = OrderedDict()

    def get_name(self):
        return self.name

    def add_grouping(self, grouping, count, percent):
        freqs = Frequencies(count, percent)
        self.groupings[str(grouping)] = freqs

    def get_count(self, grouping):
        return self.groupings[grouping].count

    def get_percent(self, grouping):
        return self.groupings[grouping].percent

    def get_groupings(self):
        return self.groupings.keys()

    def length_groups(self):
        return len(self.groupings.keys())

class Frequencies(object):

    def __init__ (self, count, percent):
        self.__count = long(count)
        self.__percent = float(percent)

    @property
    def count(self):
        return self.__count

    @property
    def percent(self):
        return self.__percent
