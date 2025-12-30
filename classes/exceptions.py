class MapGenerationError(Exception):
    """Raised when the map cannot be generated."""
    pass

class AuthFailedException(Exception):
    """Raised when the API authentication fails."""
    pass