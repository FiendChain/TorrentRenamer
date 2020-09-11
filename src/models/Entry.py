class Entry:
    def __init__(self, old_path, new_path, enabled=True):
        self.enabled = enabled
        self.old_path = old_path
        self.new_path = new_path