from text_processing import *


class SVO:
    def __init__(self, subject='', action='', obj=''):
        self.subject = self.get_formatted_value(subject)
        self.action = self.get_formatted_value(action)
        self.object = self.get_formatted_value(obj)

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.subject, self.action, self.object)

    @property
    def subject(self):
        return self.subject

    @subject.setter
    def subject(self, value):
        self.subject = self.get_formatted_value(value)

    @property
    def action(self):
        return self.action

    @action.setter
    def action(self, value):
        self.action = self.get_formatted_value(value)

    @property
    def object(self):
        return self.object

    @object.setter
    def object(self, value):
        self.object = self.get_formatted_value(value)

    @staticmethod
    def get_formatted_value(value):
        return lemmatize_word(value.lower()) if value is not None else None

    def valid(self):
        return self.subject is not None and self.action is not None and self.object is not None
