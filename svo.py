class SVO:

    def __init__(self, subject='', action='', obj=''):
        self.subject = subject
        self.action = action
        self.object = obj

    def __str__(self):
        return '({0}, {1}, {2})'.format(self.subject, self.action, self.object)

    @property
    def subject(self):
        return self.subject

    @subject.setter
    def subject(self, value):
        self.subject = value

    @property
    def action(self):
        return self.action

    @action.setter
    def action(self, value):
        self.action = value

    @property
    def object(self):
        return self.object

    @object.setter
    def object(self, value):
        self.object = value

