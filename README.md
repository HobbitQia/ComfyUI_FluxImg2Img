# ComfyUI_FluxImg2Img

- **Flux Model Loader**: 用于加载 Flux 模型和 LoRA 适配器
- **Flux Image Processor**: 执行图像到图像的生成处理

## 🔧 安装步骤

1. **克隆项目**
   ```bash
   git clone <repository-url>
   cd ComfyUI_FluxImg2Img
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **复制到ComfyUI**
   ```bash
   cp -r custom_nodes/ComfyUI-FluxImg2Img /path/to/ComfyUI/custom_nodes/
   ```

4. **重启ComfyUI**
   重启 ComfyUI 服务器以加载新的自定义节点。

## 🎯 使用方法

### 1. Flux Model Loader 节点

**功能**: 加载Flux模型和LoRA适配器

**参数设置**:
- `model_path` (STRING): Flux 模型路径
  - 例子: `/mnt/public/qjj/weights/FLUX.1-dev`
  - 说明: 指向 Flux 基础模型的目录路径

- `lora_path` (STRING): LoRA 适配器路径
  - 例子: `/mnt/public/qjj/ai-toolkit/output/my_first_flux_lora_0728-brachelet/my_first_flux_lora_0728-brachelet.safetensors`
  - 说明: 指向 LoRA 权重文件的路径

**输出**:
- `pipeline` (FLUX_PIPELINE): 加载完成的模型管道

### 2. Flux Image Processor 节点

**功能**: 执行图像到图像的生成处理

**参数设置**:

#### 基础参数

- `pipeline` (FLUX_PIPELINE): 从 Flux Model Loader 输出的模型管道
- `image` (IMAGE): 输入图像

#### 生成参数

- `prompt` (STRING): 文本提示词
- `strength` (FLOAT): 生成强度
  - 范围: 0.0 - 1.0
  - 默认值: 0.8
  - 步长: 0.01

- `steps` (INT): 推理步数
  - 默认值: 50

- `guidance_scale` (FLOAT): 引导比例
  - 范围: 0.0 - 20.0
  - 默认值: 5.0
- `seed` (INT): 随机种子
  - 范围: -1 到 0xffffffffffffffff
  - 默认值: 0
  - 说明: -1表示随机种子，其他值用于可重复的生成结果
- `num_images_per_prompt` (INT): 每提示生成图像数量
  - 范围: 1 - 100
  - 默认值: 1

## 📁 文件结构

```
ComfyUI_FluxImg2Img/
├── custom_nodes/
│   └── ComfyUI-FluxImg2Img/
│       ├── __init__.py          # 节点注册文件
│       └── flux.py              # 主要功能实现
├── comfyui_fluximg2img.json    # 示例工作流
├── requirements.txt             # 依赖包列表
└── README.md                   # 项目文档
```