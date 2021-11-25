

class DupFile:
    def __init__(self, name, size, file_type = None):
        self.name = name
        self.size = size
        self.file_type = file_type

    def __repr__(self):
        return f"name={self.name}, size={self.size}, file_type={self.file_type}"

