from text_processing import *


class SVO:
    def __init__(self, subject='', subject_params=None, action='', action_params=None, obj='', obj_params=None):
        if subject_params is None:
            subject_params = []
        if action_params is None:
            action_params = []
        if obj_params is None:
            obj_params = []
        self.subject = self.get_formatted_value(subject)
        self.subject_params = [(param[0], self.get_formatted_value(param[1])) for param in subject_params]
        self.action = self.get_formatted_value(action)
        self.action_params = [(param[0], self.get_formatted_value(param[1])) for param in action_params]
        self.object = self.get_formatted_value(obj)
        self.object_params = [(param[0], self.get_formatted_value(param[1])) for param in obj_params]

    def __str__(self):
        return '{0}: {1},\n{2}: {3},\n{4}: {5}\n'.format(self.subject, self.subject_params, self.action,
                                                                     self.action_params, self.object,
                                                                     self.object_params)

    @property
    def subject(self):
        return self.subject

    @subject.setter
    def subject(self, value):
        self.subject = self.get_formatted_value(value)

    @property
    def subject_params(self):
        return self.subject_params

    @subject_params.setter
    def subject_params(self, params):
        self.subject_params = [(param[0], self.get_formatted_value(param[1])) for param in params]

    @property
    def action(self):
        return self.action

    @action.setter
    def action(self, value):
        self.action = self.get_formatted_value(value)

    @property
    def action_params(self):
        return self.action_params

    @action_params.setter
    def action_params(self, params):
        self.action_params = lemmatize_words(params)

    @property
    def object(self):
        return self.object

    @object.setter
    def object(self, value):
        self.object = self.get_formatted_value(value)

    @property
    def object_params(self):
        return self.object_params

    @object_params.setter
    def object_params(self, params):
        self.object_params = lemmatize_words(params)

    @staticmethod
    def get_formatted_value(value):
        return lemmatize_word(value.lower()) if value is not None else None

    def valid(self):
        return self.subject is not None and self.action is not None and self.object is not None
