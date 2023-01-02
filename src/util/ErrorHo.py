class FileAlreadyExists(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return self.msg


class Anythingdonthave(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return self.msg


class UserNotFound(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return self.msg


class FileNoExists(Exception):
    def __init__(self, msg):
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return self.msg
