import ctypes
import subprocess
import os
from . import get_bin_dir
from .logging import get_logger

logger = get_logger(\"diagnostics\")

def run_diagnostic():
    \"\"\"Verify that the GPU and CUDA DLLs are working correctly.\"\"\"
    logger.info(\"Starting GPU/CUDA diagnostics...\")
    results = {
        \"gpu_present\": False,
        \"driver_version\": \"Unknown\",
        \"dll_load_status\": \"Not Tested\",
        \"vram_total_mb\": 0,
        \"vram_free_mb\": 0
    }
    
    # 1. Check for nvidia-smi
    try:
        smi = subprocess.check_output([\"nvidia-smi\", \"--query-gpu=driver_version,memory.total,memory.free\", \"--format=csv,noheader,nounits\"], encoding='utf-8')
        parts = smi.strip().split(',')
        results[\"gpu_present\"] = True
        results[\"driver_version\"] = parts[0].strip()
        results[\"vram_total_mb\"] = int(parts[1].strip())
        results[\"vram_free_mb\"] = int(parts[2].strip())
        logger.debug(f\"NVIDIA GPU found. Driver: {results['driver_version']}\")
    except Exception as e:
        logger.warning(f\"nvidia-smi failed or not found: {e}\")
        results[\"gpu_present\"] = False

    # 2. Try loading the CUDA Runtime DLL
    try:
        bin_dir = get_bin_dir()
        dll_name = f\"cudart64_12.dll\"
        dll_path = str(bin_dir / dll_name)
        if os.path.exists(dll_path):
            logger.debug(f\"Attempting to load {dll_name} from {bin_dir}\")
            ctypes.WinDLL(dll_path)
            results[\"dll_load_status\"] = \"Success\"
            logger.info(\"CUDA DLL load successful.\")
        else:
            results[\"dll_load_status\"] = f\"Missing: {dll_name}\"
            logger.error(f\"CUDA DLL not found in backend bin directory: {dll_path}\")
    except Exception as e:
        results[\"dll_load_status\"] = f\"Error: {str(e)}\"
        logger.error(f\"Failed to load CUDA DLL: {e}\")

    return results
