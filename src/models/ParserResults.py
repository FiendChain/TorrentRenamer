from .Entry import Entry

# wrap raw dict from parser into usable model
class ParserResults:
    def __init__(self, p):
        self.renames = [Entry(old, new) for old, new in p.get('renames', [])]
        self.conflicts = [Entry(old, new, enabled=False) for old, new in p.get('conflicts', [])]
        self.ignores = p.get('ignores', [])
        self.deletes = p.get('deletes', [])
        self.completed = p.get('completed', [])
