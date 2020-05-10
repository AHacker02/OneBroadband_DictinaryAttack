class User:
    def __init__(self, username, password='1234',mac=None,plan=None):
        self.username = username
        self.password = password
        self.mac = mac
        self.plan = plan

    def __str__(self):
        return f'{self.username},{self.mac},{self.plan}\n'

    def __bool__(self):
        return self.mac is not None
