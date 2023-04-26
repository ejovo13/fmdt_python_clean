class GroundTruthError(Exception):
    """Raised when a video doesn't have any ground truths in our data base"""
    pass

class LogError(Exception):
    """Raised when we have issues with the `log_path` parameter"""
    pass

class DatabaseError(Exception):
    """Raised when there is an issue retrieving information from our database"""
    pass