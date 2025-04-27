class Singer:
    def __init__(self, name, song):
        self.name = name
        self.song = song
        self.last_performance = None

    def __repr__(self):
        return f"{self.name} singing '{self.song}'"


class Queue:
    def __init__(self):
        self.line = []

    def add_singer(self, singer):
        self.line.append(singer)

    def next_singer(self):
        if self.line:
            return self.line.pop(0)
        return None

    def show_queue(self):
        return [str(s) for s in self.line]
