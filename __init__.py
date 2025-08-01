# __init__.py

# Import all node classes from their respective files
from .flux import FluxModelLoader
from .flux import FluxImageProcessor

# Create the mapping dictionaries for ComfyUI
NODE_CLASS_MAPPINGS = {
    "FluxModelLoader": FluxModelLoader,
    "FluxImageProcessor": FluxImageProcessor,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxModelLoader": "Flux Model Loader",
    "FluxImageProcessor": "Flux Image Processor",
}

print("✅ Loaded Advanced Relief Custom Nodes")