# aurarouter-cuda12

**AuraRouter Stable GPU Backend (CUDA 12.4)**

This package is a "sidecar" for **AuraRouter**. It contains the pre-compiled binary payload required to run local LLMs on older NVIDIA GPUs or systems with legacy drivers.

## What's inside?
- `llama-server.exe`: Compiled with CUDA 12.4 support.
- `ggml-cuda.dll`: Optimized kernels for NVIDIA architectures.
- `cudart64_12.dll` & `cublas64_12.dll`: Required NVIDIA runtime libraries.

## Requirements
- **Hardware**: NVIDIA GPU.
- **Drivers**: NVIDIA Driver version **525.60** or higher.
- **AuraRouter**: Must be installed in the same environment.

## Usage
Simply install this package into the same virtual environment as `aurarouter`:

```bash
pip install aurarouter-cuda12
```

AuraRouter's `BinaryManager` will automatically detect this package and use it for local inference. It is prioritized over CPU-based backends but lower than `aurarouter-cuda13`.
