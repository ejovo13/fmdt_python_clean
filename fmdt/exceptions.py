class GroundTruthError(Exception):
    """Raised when a video doesn't have any ground truths in our data base"""
    pass

class LogError(Exception):
    """Raised when we have issues with the `log_path` parameter"""
    pass

class DatabaseError(Exception):
    """Raised when there is an issue retrieving information from our database"""
    pass

class AbstractExecutableArgsError(Exception):
    """Raised when an implementer of the ABC AbstractExecutableArgs does not fulfill
    the required condiitons
    """

class AbstractResultError(Exception):
    """Raised when an implementer of the ABC AbstractResult does not fulfull a necessary condition"""