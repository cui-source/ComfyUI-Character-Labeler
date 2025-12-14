import torch
import comfy
import json
import os
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from typing import Dict, List, Tuple, Any, Optional
import folder_paths

# 确保配置目录存在
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "configs")
os.makedirs(CONFIG_DIR, exist_ok=True)

# 工具导入
from .utils.variable_processor import variable_processor
from .utils.label_generator import LabelGenerator


class CLIPVisionLoaderWrapper:
    """CLIP视觉模型加载器包装器"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_name": (folder_paths.get_filename_list("clip_vision"),),
            }
        }
    
    RETURN_TYPES = ("CLIP_VISION",)
    RETURN_NAMES = ("clip_vision",)
    FUNCTION = "load_clip"
    CATEGORY = "character_labeler/clip"
    
    def load_clip(self, clip_name):
        from comfy.clip_vision import load_clipvision
        clip_path = folder_paths.get_full_path("clip_vision", clip_name)
        clip_vision = load_clipvision(clip_path)
        return (clip_vision,)


class CLIPVisionEncodeWrapper:
    """CLIP视觉编码器包装器"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_vision": ("CLIP_VISION",),
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("CLIP_VISION_OUTPUT",)
    RETURN_NAMES = ("clip_vision_output",)
    FUNCTION = "encode"
    CATEGORY = "character_labeler/clip"
    
    def encode(self, clip_vision, image):
        # 这里使用ComfyUI的CLIP视觉编码器
        # 注意：实际上ComfyUI的CLIP视觉编码器输出可能需要特殊处理
        # 这里我们返回一个模拟的CLIP视觉特征
        output = {
            "image_features": image.mean(dim=[1, 2, 3], keepdim=True),  # 简化处理
            "clip_vision": clip_vision
        }
        return (output,)


class CLIPImageAnalyzer:
    """CLIP图像分析器节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_vision_output": ("CLIP_VISION_OUTPUT",),
                "confidence_threshold": ("FLOAT", {"default": 0.7, "min": 0.0, "max": 1.0, "step": 0.01}),
                "analysis_mode": (["快速分析", "详细分析"], {"default": "快速分析"}),
            }
        }
    
    RETURN_TYPES = ("DICT", "STRING", "CLIP_VISION_OUTPUT")
    RETURN_NAMES = ("clip_analysis", "analysis_text", "clip_vision_output")
    FUNCTION = "analyze_image"
    CATEGORY = "character_labeler/clip"
    
    def analyze_image(self, clip_vision_output, confidence_threshold, analysis_mode):
        # 这里可以添加真正的CLIP分析逻辑
        # 目前使用模拟数据
        
        # 定义特征文本（中英文对照，便于后续处理）
        feature_texts = {
            "长发": "long hair",
            "短发": "short hair", 
            "卷发": "curly hair",
            "直发": "straight hair",
            "马尾": "ponytail",
            "双马尾": "twin tails",
            "微笑": "smile",
            "愤怒": "angry", 
            "悲伤": "sad",
            "惊讶": "surprised",
            "害羞": "shy",
            "站立": "standing",
            "坐姿": "sitting", 
            "奔跑": "running",
            "跳跃": "jumping",
            "城市背景": "city background",
            "自然背景": "nature background",
            "室内": "indoor",
            "室外": "outdoor",
            "白天": "daytime", 
            "夜晚": "night",
            "黄昏": "dusk",
            "动漫风格": "anime style",
            "写实风格": "realistic style",
            "油画风格": "oil painting style",
            "男性": "male",
            "女性": "female", 
            "年轻": "young",
            "老年": "old"
        }
        
        # 模拟分析结果
        results = {}
        analysis_text = "CLIP分析结果: "
        
        # 根据分析模式选择分析的特征数量
        if analysis_mode == "快速分析":
            num_features = 8
        else:
            num_features = 15
        
        # 模拟置信度分数
        features_to_check = list(feature_texts.keys())[:num_features]
        for feature in features_to_check:
            confidence = np.random.uniform(0.5, 0.95)
            if confidence > confidence_threshold:
                results[feature] = {
                    "confidence": float(confidence),
                    "english": feature_texts[feature]
                }
                analysis_text += f"{feature}({confidence:.2f}), "
        
        analysis_text = analysis_text.rstrip(", ") + "。"
        
        return (results, analysis_text, clip_vision_output)


class CoreVariableSelector:
    """核心变量选择器节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        # 使用配置管理器加载核心变量
        core_vars = variable_processor.load_core_variables()
        
        # 创建输入类型字典
        input_dict = {
            "required": {},
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
        
        # 为每个核心变量添加选择框
        for category, variables in core_vars.items():
            for var_name, options in variables.items():
                if options:  # 确保选项列表不为空
                    input_dict["required"][var_name] = (options, {"default": options[0]})
        
        return input_dict
    
    RETURN_TYPES = ("DICT", "STRING")
    RETURN_NAMES = ("core_variables", "core_variables_text")
    FUNCTION = "select_core_variables"
    CATEGORY = "character_labeler/variables"
    
    def select_core_variables(self, **kwargs):
        core_vars = variable_processor.load_core_variables()
        selected = {}
        text_parts = []
        
        for category, variables in core_vars.items():
            selected[category] = {}
            for var_name in variables.keys():
                if var_name in kwargs:
                    value = kwargs[var_name]
                    selected[category][var_name] = value
                    # 中文显示
                    text_parts.append(f"{var_name}: {value}")
        
        variables_text = "核心变量: " + "，".join(text_parts)
        return (selected, variables_text)


class VariableVariableSelector:
    """可变变量选择器节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        # 使用配置管理器加载可变变量
        var_vars = variable_processor.load_variable_variables()
        
        input_dict = {
            "required": {},
            "hidden": {"unique_id": "UNIQUE_ID"}
        }
        
        # 为每个可变变量添加选择框
        for category, subcategories in var_vars.items():
            for sub_name, levels in subcategories.items():
                if isinstance(levels, dict) and "一级" in levels:
                    # 创建一级选择框
                    level1_options = levels["一级"]
                    if level1_options:
                        input_dict["required"][f"{category}_{sub_name}_level1"] = (
                            level1_options, 
                            {"default": level1_options[0]}
                        )
                    
                    # 如果有二级选项，创建二级选择框
                    if "二级" in levels and isinstance(levels["二级"], dict):
                        # 获取默认的一级值，用于确定二级选项
                        default_level1 = level1_options[0] if level1_options else ""
                        level2_options = levels["二级"].get(default_level1, [])
                        
                        if level2_options:
                            input_dict["required"][f"{category}_{sub_name}_level2"] = (
                                level2_options,
                                {"default": level2_options[0] if level2_options else ""}
                            )
        
        return input_dict
    
    RETURN_TYPES = ("DICT", "STRING")
    RETURN_NAMES = ("variable_variables", "variable_variables_text")
    FUNCTION = "select_variable_variables"
    CATEGORY = "character_labeler/variables"
    
    def select_variable_variables(self, **kwargs):
        var_vars = variable_processor.load_variable_variables()
        selected = {}
        text_parts = []
        
        for category, subcategories in var_vars.items():
            selected[category] = {}
            for sub_name, levels in subcategories.items():
                if isinstance(levels, dict) and "一级" in levels:
                    key_level1 = f"{category}_{sub_name}_level1"
                    key_level2 = f"{category}_{sub_name}_level2"
                    
                    if key_level1 in kwargs:
                        value_level1 = kwargs[key_level1]
                        selected[category][sub_name] = {
                            "一级": value_level1,
                            "二级": ""
                        }
                        
                        # 如果有二级选择且存在对应选项
                        if key_level2 in kwargs and kwargs[key_level2]:
                            value_level2 = kwargs[key_level2]
                            selected[category][sub_name]["二级"] = value_level2
                            text_parts.append(f"{sub_name}: {value_level1}({value_level2})")
                        else:
                            text_parts.append(f"{sub_name}: {value_level1}")
        
        variables_text = "可变变量: " + "，".join(text_parts)
        return (selected, variables_text)


class CharacterLabelGenerator:
    """人物标签生成器主节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip_analysis": ("DICT",),
                "core_variables": ("DICT",),
                "variable_variables": ("DICT",),
                "output_format": (["标签列表", "详细描述", "JSON格式", "提示词格式"], {"default": "标签列表"}),
                "include_clip_analysis": (["是", "否"], {"default": "是"}),
                "separator": ("STRING", {"default": ", ", "multiline": False}),
                "language": (["中文", "英文"], {"default": "中文"}),
            },
            "optional": {
                "additional_prompt": ("STRING", {"default": "", "multiline": True}),
                "clip_vision_output": ("CLIP_VISION_OUTPUT", {"optional": True}),
            }
        }
    
    RETURN_TYPES = ("STRING", "STRING")
    RETURN_NAMES = ("character_labels", "formatted_labels")
    FUNCTION = "generate_labels"
    CATEGORY = "character_labeler/main"
    
    def generate_labels(self, clip_analysis, core_variables, variable_variables, 
                       output_format, include_clip_analysis, separator, language, 
                       additional_prompt="", clip_vision_output=None):
        
        # 使用LabelGenerator工具生成标签
        labels, formatted = LabelGenerator.generate_labels(
            core_variables=core_variables,
            variable_variables=variable_variables,
            clip_analysis=clip_analysis if include_clip_analysis == "是" else None,
            additional_prompt=additional_prompt,
            output_format=output_format,
            language=language,
            separator=separator,
            include_clip=(include_clip_analysis == "是")
        )
        
        return (labels, formatted)


class ConfigManager:
    """配置管理器节点"""
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "action": (["重新加载配置", "导出配置", "重置为默认", "查看配置"], {"default": "重新加载配置"}),
                "config_type": (["核心变量", "可变变量", "全部"], {"default": "全部"}),
            },
            "optional": {
                "import_config": ("STRING", {"default": "", "multiline": True}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status_message",)
    FUNCTION = "manage_config"
    CATEGORY = "character_labeler/config"
    
    def manage_config(self, action, config_type, import_config=""):
        message = ""
        
        try:
            if action == "重新加载配置":
                # 重新加载配置
                message = "✅ 配置已重新加载"
                
                if config_type == "核心变量" or config_type == "全部":
                    core_config = variable_processor.load_core_variables()
                    message += f"\n📊 核心变量配置已加载，共{sum(len(v) for v in core_config.values())}个选项"
                
                if config_type == "可变变量" or config_type == "全部":
                    var_config = variable_processor.load_variable_variables()
                    message += f"\n🎭 可变变量配置已加载"
            
            elif action == "导出配置":
                # 导出配置
                if config_type == "核心变量" or config_type == "全部":
                    core_config = variable_processor.load_core_variables()
                    core_config_path = os.path.join(CONFIG_DIR, "core_variables.json")
                    with open(core_config_path, 'w', encoding='utf-8') as f:
                        json.dump(core_config, f, ensure_ascii=False, indent=2)
                    message += f"📤 核心变量配置已导出到: {core_config_path}\n"
                
                if config_type == "可变变量" or config_type == "全部":
                    var_config = variable_processor.load_variable_variables()
                    var_config_path = os.path.join(CONFIG_DIR, "variable_variables.json")
                    with open(var_config_path, 'w', encoding='utf-8') as f:
                        json.dump(var_config, f, ensure_ascii=False, indent=2)
                    message += f"📤 可变变量配置已导出到: {var_config_path}"
            
            elif action == "重置为默认":
                # 重置为默认配置
                if config_type == "核心变量" or config_type == "全部":
                    variable_processor._create_default_core_config()
                    message += "🔄 核心变量配置已重置为默认值\n"
                
                if config_type == "可变变量" or config_type == "全部":
                    variable_processor._create_default_variable_config()
                    message += "🔄 可变变量配置已重置为默认值"
            
            elif action == "查看配置":
                # 查看当前配置
                if config_type == "核心变量" or config_type == "全部":
                    core_config = variable_processor.load_core_variables()
                    message += "📋 核心变量配置:\n"
                    for category, vars in core_config.items():
                        message += f"  {category}:\n"
                        for var_name, options in vars.items():
                            message += f"    - {var_name}: {len(options)}个选项\n"
                    message += "\n"
                
                if config_type == "可变变量" or config_type == "全部":
                    var_config = variable_processor.load_variable_variables()
                    message += "📋 可变变量配置:\n"
                    for category, subs in var_config.items():
                        message += f"  {category}:\n"
                        for sub_name, levels in subs.items():
                            if isinstance(levels, dict) and "一级" in levels:
                                count = len(levels["一级"])
                                message += f"    - {sub_name}: {count}个一级选项\n"
            
            # 添加配置文件路径信息
            core_path = os.path.join(CONFIG_DIR, "core_variables.json")
            var_path = os.path.join(CONFIG_DIR, "variable_variables.json")
            message += f"\n\n📁 配置文件路径:\n  核心变量: {core_path}\n  可变变量: {var_path}"
            
        except Exception as e:
            message = f"❌ 配置管理出错: {str(e)}"
        
        return (message,)


# 节点映射
NODE_CLASS_MAPPINGS = {
    # CLIP相关节点
    "CLIPVisionLoaderWrapper": CLIPVisionLoaderWrapper,
    "CLIPVisionEncodeWrapper": CLIPVisionEncodeWrapper,
    "CLIPImageAnalyzer": CLIPImageAnalyzer,
    
    # 变量选择器节点
    "CoreVariableSelector": CoreVariableSelector,
    "VariableVariableSelector": VariableVariableSelector,
    
    # 主节点
    "CharacterLabelGenerator": CharacterLabelGenerator,
    
    # 配置管理节点
    "ConfigManager": ConfigManager,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # CLIP相关节点
    "CLIPVisionLoaderWrapper": "🔤 CLIP视觉模型加载器",
    "CLIPVisionEncodeWrapper": "🔤 CLIP视觉编码器",
    "CLIPImageAnalyzer": "🔤 CLIP图像分析器",
    
    # 变量选择器节点
    "CoreVariableSelector": "🎯 核心变量选择器",
    "VariableVariableSelector": "🎯 可变变量选择器",
    
    # 主节点
    "CharacterLabelGenerator": "✨ 人物标签生成器",
    
    # 配置管理节点
    "ConfigManager": "⚙️ 配置管理器",
}