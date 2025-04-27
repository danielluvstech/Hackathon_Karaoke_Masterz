class Singer:
    """Represents a singer in the karaoke app."""
    def __init__(self, id, name, song_title, nickname=None):
        self.id = id
        self.name = name
        self.song_title = song_title
        self.nickname = nickname

    def __str__(self):
        return f"{self.name} (ID: {self.id}) singing '{self.song_title}'"

class QueueEntry:
    """Represents an entry in the karaoke queue."""
    def __init__(self, id, singer_id, position):
        self.id = id
        self.singer_id = singer_id
        self.position = position

    def __str__(self):
        return f"Queue Entry {self.id}: Singer ID {self.singer_id} at position {self.position}"