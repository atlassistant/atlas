class Skill:
    """Skill represents a skill backend in atlas.
    """

    def __init__(self, path, name, cmd, version=None, description=None, author=None, meta=None):
        """Constructs a new skill.
        """

        self.path = path
        self.name = name
        self.cmd = cmd
        self.version = version
        self.description = description
        self.author = author

    def __str__(self):
        return '%s %s by %s' % (self.name, self.version, self.author)