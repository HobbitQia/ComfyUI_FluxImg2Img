import torch
import numpy as np
from PIL import Image
from diffusers import FluxImg2ImgPipeline
# import folder_paths
import comfy.utils

# ========================= 模块1: Flux模型加载器 =========================
class FluxModelLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_path": ("STRING", {"default": "/mnt/public/qjj/weights/FLUX.1-dev"}),
                "lora_path": ("STRING", {"default": "/mnt/public/qjj/ai-toolkit/output/my_first_flux_lora_0728-brachelet/my_first_flux_lora_0728-brachelet.safetensors"}),
            }
        }
    
    RETURN_TYPES = ("FLUX_PIPELINE",)
    RETURN_NAMES = ("pipeline",)
    FUNCTION = "load_model"
    CATEGORY = "Flux"

    def load_model(self, model_path, lora_path):
        # 加载基础模型
        pipeline = FluxImg2ImgPipeline.from_pretrained(
            model_path, 
            torch_dtype=torch.bfloat16
        )
        
        # 加载LoRA适配器
        pipeline.load_lora_weights(lora_path)
        
        # 将模型移动到GPU
        pipeline.to('cuda')
        return (pipeline,)

# ======================= 模块2: Flux图像到图像处理 =======================
class FluxImageProcessor:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "pipeline": ("FLUX_PIPELINE",),
                "image": ("IMAGE",),
                "prompt": ("STRING", {"multiline": True, "default": "front view, bracelet, white background"}),
                "strength": ("FLOAT", {"default": 0.8, "min": 0.0, "max": 1.0, "step": 0.01}),
                "steps": ("INT", {"default": 50, "min": 1, "max": 100}),
                "guidance_scale": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 20.0}),
                "seed": ("INT", {"default": 0, "min": -1, "max": 0xffffffffffffffff}),
                "width": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "height": ("INT", {"default": 1024, "min": 64, "max": 2048}),
                "num_images_per_prompt": ("INT", {
                    "default": 1,
                    "min": 1,
                    "max": 100,
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    FUNCTION = "process_image"
    CATEGORY = "Flux"

    def process_image(self, pipeline, image, prompt, strength, steps, guidance_scale, seed, width, height, num_images_per_prompt):
        # 转换ComfyUI图像为PIL格式
        image = image[0].numpy() * 255.0
        pil_image = Image.fromarray(image.astype(np.uint8))
        
        # 处理种子值（-1表示随机）
        generator = None
        if seed != -1:
            generator = torch.Generator(device='cuda').manual_seed(seed)
        
        # 执行图像生成
        result = pipeline(
            prompt=prompt,
            image=pil_image,
            strength=strength,
            num_inference_steps=steps,
            guidance_scale=guidance_scale,
            num_images_per_prompt=num_images_per_prompt,
            width=width,
            height=height,
            generator=generator,
            max_sequence_length=512
        ).images

        pil_images = result
        images_tensor = []

        for image in pil_images:
            # 确保是RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')
            image_np = np.array(image).astype(np.float32) / 255.0
            image_tensor = torch.from_numpy(image_np).unsqueeze(0)  # 添加批次维度
            images_tensor.append(image_tensor)
        if len(images_tensor) == 0:
            # 如果没有生成图像，返回一个空张量（避免错误）
            # 注意：实际使用中应避免空张量，这里只是示例
            images_out = torch.zeros((0, 64, 64, 3), dtype=torch.float32)
        else:
            images_out = torch.cat(images_tensor, dim=0)
        return (images_out,)
        
        return (result_tensor,)

# 注册节点
NODE_CLASS_MAPPINGS = {
    "FluxModelLoader": FluxModelLoader,
    "FluxImageProcessor": FluxImageProcessor
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxModelLoader": "Flux Model Loader",
    "FluxImageProcessor": "Flux Image Processor"
}