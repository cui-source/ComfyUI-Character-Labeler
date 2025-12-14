"""
CLIP分析器工具模块
"""

import numpy as np
import torch
from typing import Dict, List, Tuple, Any
import comfy.clip_vision

class CLIPAnalyzerTool:
    """CLIP分析器工具类"""
    
    def __init__(self):
        self.feature_texts_cn = {
            "人物": ["长发", "短发", "卷发", "直发", "马尾", "双马尾", "丸子头", "男性", "女性", "年轻", "老年"],
            "表情": ["微笑", "愤怒", "悲伤", "惊讶", "平静", "害羞", "严肃", "调皮", "困惑", "恐惧"],
            "姿势": ["站立", "坐姿", "卧姿", "跪姿", "跳跃", "奔跑", "飞行", "游泳"],
            "环境": ["城市", "荒野", "室内", "室外", "白天", "夜晚", "黄昏", "黎明"],
            "风格": ["动漫", "写实", "油画", "水彩", "像素", "卡通", "水墨", "赛博朋克"],
            "服装": ["和服", "西装", "裙子", "T恤", "盔甲", "制服", "泳装", "礼服"]
        }
        
        self.feature_texts_en = {
            "person": ["long hair", "short hair", "curly hair", "straight hair", "ponytail", "twin tails", "bun", "male", "female", "young", "old"],
            "expression": ["smiling", "angry", "sad", "surprised", "calm", "shy", "serious", "playful", "confused", "fear"],
            "pose": ["standing", "sitting", "lying", "kneeling", "jumping", "running", "flying", "swimming"],
            "environment": ["city", "wilderness", "indoor", "outdoor", "daytime", "night", "dusk", "dawn"],
            "style": ["anime", "realistic", "oil painting", "watercolor", "pixel", "cartoon", "ink wash", "cyberpunk"],
            "clothing": ["kimono", "suit", "dress", "t-shirt", "armor", "uniform", "swimsuit", "gown"]
        }
    
    def analyze_with_clip(self, clip_vision_model, image_tensor, language="中文"):
        """
        使用CLIP模型分析图像
        
        Args:
            clip_vision_model: CLIP视觉模型
            image_tensor: 图像张量 [1, H, W, 3]
            language: 语言选择 ("中文" 或 "英文")
            
        Returns:
            Dict: 分析结果
            str: 分析文本
        """
        # 这里应该实现真正的CLIP分析
        # 目前返回模拟数据
        
        # 选择语言
        if language == "英文":
            features = self.feature_texts_en
        else:
            features = self.feature_texts_cn
        
        # 模拟分析结果
        results = {}
        for category, texts in features.items():
            for text in texts[:3]:  # 每个类别取前3个
                # 模拟置信度
                confidence = np.random.uniform(0.4, 0.95)
                results[text] = {
                    "confidence": float(confidence),
                    "category": category,
                    "language": language
                }
        
        # 生成分析文本
        analysis_text = self._generate_analysis_text(results, language)
        
        return results, analysis_text
    
    def _generate_analysis_text(self, results, language):
        """生成分析文本"""
        if language == "英文":
            text = "CLIP analysis detected: "
            for feature, data in list(results.items())[:5]:  # 显示前5个
                text += f"{feature}({data['confidence']:.2f}), "
            text = text.rstrip(", ") + "."
        else:
            text = "CLIP分析检测到: "
            for feature, data in list(results.items())[:5]:
                text += f"{feature}({data['confidence']:.2f}), "
            text = text.rstrip(", ") + "。"
        
        return text
    
    def filter_results_by_threshold(self, results, threshold=0.7):
        """按阈值过滤结果"""
        filtered = {}
        for feature, data in results.items():
            if data["confidence"] >= threshold:
                filtered[feature] = data
        return filtered
    
    def get_top_features(self, results, top_n=10):
        """获取置信度最高的特征"""
        sorted_features = sorted(results.items(), key=lambda x: x[1]["confidence"], reverse=True)
        return dict(sorted_features[:top_n])


# 创建全局实例
clip_analyzer = CLIPAnalyzerTool()