class StudentNotFoundException(Exception):

    def __init__(self, message="Student not found"):
        self.message = message
        super().__init__(self.message)