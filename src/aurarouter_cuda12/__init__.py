\"\"\"AuraRouter CUDA 12.4 Backend Package\"\"\"

import os
import sys
import platform
from pathlib import Path
from .logging import get_logger

logger = get_logger()

def get_bin_dir() -> Path:
    \"\"\"Return the absolute path to the bundled binaries directory for the current platform.\"\"\"
    machine = platform.machine().lower()
    
    if sys.platform == \"win32\" and machine in (\"amd64\", \"x86_64\"):
        plat = \"win-x64\"
    elif sys.platform == \"linux\" and machine == \"x86_64\":
        plat = \"linux-x64\"
    elif sys.platform == \"darwin\" and machine in (\"x86_64\", \"arm64\"):
        plat = \"macos-x64\"
    else:
        raise RuntimeError(f\"Unsupported platform for this backend package: {sys.platform}/{machine}\")
        
    return Path(__file__).parent / \"bin\" / plat

def setup_runtime_environment():
    \"\"\"Configure the environment (like PATH/DLL search paths) to ensure binaries can load their dependencies.\"\"\"
    try:
        bin_dir = get_bin_dir()
        if sys.platform == \"win32\" and hasattr(os, \"add_dll_directory\"):
            # Ensure sibling DLLs (like cudart, cublas) are discoverable on Windows
            logger.debug(f\"Adding DLL directory: {bin_dir}\")
            os.add_dll_directory(str(bin_dir))
        
        # Add to PATH as a fallback for subprocesses
        logger.debug(f\"Prepending to PATH: {bin_dir}\")
        os.environ[\"PATH\"] = str(bin_dir) + os.pathsep + os.environ.get(\"PATH\", \"\")
    except Exception as e:
        logger.error(f\"Failed to setup runtime environment: {e}\")
