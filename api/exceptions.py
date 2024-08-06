class UniqueConstraintViolation(Exception):
    """Excepción lanzada cuando se viola una restricción de unicidad."""
    pass

class NotFoundException(Exception):
    """Excepción lanzada cuando un elemento no se encuentra en la base de datos."""
    pass

class DatabaseOperationException(Exception):
    """Excepción general para errores de operaciones de base de datos."""
    pass