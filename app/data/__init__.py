from .json_storage import JsonStorage

# Create a singleton instance for development
storage = JsonStorage()

__all__ = ['storage', 'JsonStorage'] 