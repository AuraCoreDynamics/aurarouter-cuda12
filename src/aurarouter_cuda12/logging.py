import logging

def get_logger(name: str = None) -> logging.Logger:
    \"\"\"Return a logger prefixed with the AuraRouter backend namespace.\"\"\"
    base_name = \"AuraRouter.Backend.CUDA12\"
    if name:
        return logging.getLogger(f\"{base_name}.{name}\")
    return logging.getLogger(base_name)
