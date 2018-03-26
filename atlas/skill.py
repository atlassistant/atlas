class Skill:
    """Skill represents a skill backend in atlas.
    """

    def __init__(self, name, cmd, version=None, description=None, author=None, meta=None):
        """Constructs a new skill.
        """

        self.name = name
        self.cmd = cmd
        self.version = version
        self.description = description
        self.author = author