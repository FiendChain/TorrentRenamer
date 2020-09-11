from .Entry import Entry

class ParserResults:
    def __init__(self, p):
        renames = p.get('renames')
        conflicts = p.get('conflicts')
        ignores = p.get('ignores')

        self.renames = [Entry(old, new) for old, new in renames]
        self.conflicts = conflicts
        self.ignores = ignores
