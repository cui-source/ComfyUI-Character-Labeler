"""
标签生成器工具模块
"""

import json
import re
from typing import Dict, List, Tuple, Any
from datetime import datetime

class LabelGenerator:
    """标签生成器"""
    
    @staticmethod
    def generate_labels(core_variables: Dict, variable_variables: Dict, 
                       clip_analysis: Dict = None, additional_prompt: str = "",
                       output_format: str = "标签列表", language: str = "中文",
                       separator: str = ", ", include_clip: bool = True) -> Tuple[str, str]:
        """
        生成标签
        
        Args:
            core_variables: 核心变量
            variable_variables: 可变变量
            clip_analysis: CLIP分析结果
            additional_prompt: 附加提示词
            output_format: 输出格式
            language: 语言
            separator: 分隔符
            include_clip: 是否包含CLIP分析
            
        Returns:
            Tuple[str, str]: 生成的标签和格式化输出
        """
        # 1. 处理核心变量
        core_tags = LabelGenerator._process_core_variables(core_variables, language)
        
        # 2. 处理可变变量
        variable_tags = LabelGenerator._process_variable_variables(variable_variables, language)
        
        # 3. 处理CLIP分析结果
        clip_tags = []
        if include_clip and clip_analysis:
            clip_tags = LabelGenerator._process_clip_analysis(clip_analysis, language)
        
        # 4. 处理附加提示
        additional_tags = []
        if additional_prompt and additional_prompt.strip():
            additional_tags = [tag.strip() for tag in additional_prompt.split(",") if tag.strip()]
        
        # 5. 合并所有标签
        all_tags = []
        all_tags.extend(core_tags)
        all_tags.extend(variable_tags)
        all_tags.extend(clip_tags)
        all_tags.extend(additional_tags)
        
        # 6. 去重
        unique_tags = []
        seen = set()
        for tag in all_tags:
            if tag and tag not in seen:
                seen.add(tag)
                unique_tags.append(tag)
        
        # 7. 根据输出格式生成最终标签
        if output_format == "标签列表":
            result = separator.join(unique_tags)
            formatted = result
        elif output_format == "详细描述":
            result = LabelGenerator._format_detailed_description(core_tags, variable_tags, clip_tags, additional_tags, language)
            formatted = result
        elif output_format == "JSON格式":
            result = LabelGenerator._format_json(core_variables, variable_variables, clip_analysis, additional_tags)
            formatted = json.dumps(json.loads(result), ensure_ascii=False, indent=2)
        elif output_format == "提示词格式":
            result = LabelGenerator._format_prompt(unique_tags, language)
            formatted = result
        else:
            result = separator.join(unique_tags)
            formatted = result
        
        return result, formatted
    
    @staticmethod
    def _process_core_variables(core_variables: Dict, language: str = "中文") -> List[str]:
        """处理核心变量"""
        tags = []
        
        for category, variables in core_variables.items():
            for var_name, value in variables.items():
                if value:  # 只添加非空值
                    if language == "英文":
                        # 简单的中英文转换
                        en_mapping = {
                            "长发": "long hair", "短发": "short hair", "卷发": "curly hair",
                            "直发": "straight hair", "男性": "male", "女性": "female",
                            "年轻": "young", "老年": "old", "黑色": "black", "金色": "blonde",
                            "蓝色": "blue", "绿色": "green", "红色": "red", "白色": "white"
                        }
                        tag = en_mapping.get(value, value)
                    else:
                        tag = value
                    tags.append(tag)
        
        return tags
    
    @staticmethod
    def _process_variable_variables(variable_variables: Dict, language: str = "中文") -> List[str]:
        """处理可变变量"""
        tags = []
        
        for category, subcategories in variable_variables.items():
            for sub_name, levels in subcategories.items():
                level1 = levels.get("一级", "")
                level2 = levels.get("二级", "")
                
                if level1:
                    if language == "英文":
                        en_mapping = {
                            "微笑": "smiling", "愤怒": "angry", "悲伤": "sad",
                            "站立": "standing", "坐姿": "sitting", "奔跑": "running",
                            "城市": "city", "白天": "daytime", "夜晚": "night",
                            "动漫": "anime", "写实": "realistic"
                        }
                        tag = en_mapping.get(level1, level1)
                        if level2:
                            tag2 = en_mapping.get(level2, level2)
                            tag = f"{tag} ({tag2})"
                    else:
                        if level2:
                            tag = f"{level1}({level2})"
                        else:
                            tag = level1
                    
                    tags.append(tag)
        
        return tags
    
    @staticmethod
    def _process_clip_analysis(clip_analysis: Dict, language: str = "中文") -> List[str]:
        """处理CLIP分析结果"""
        tags = []
        
        if isinstance(clip_analysis, dict):
            for feature, data in clip_analysis.items():
                if isinstance(data, dict) and "confidence" in data:
                    # 这里可以根据需要过滤低置信度的特征
                    if data.get("confidence", 0) >= 0.5:
                        if language == "英文":
                            english = data.get("english", feature)
                            tags.append(english)
                        else:
                            tags.append(feature)
        
        return tags
    
    @staticmethod
    def _format_detailed_description(core_tags: List[str], variable_tags: List[str], 
                                   clip_tags: List[str], additional_tags: List[str], 
                                   language: str = "中文") -> str:
        """格式化为详细描述"""
        if language == "英文":
            sections = []
            
            if core_tags:
                sections.append(f"Character: {', '.join(core_tags)}")
            
            if variable_tags:
                sections.append(f"State & Environment: {', '.join(variable_tags)}")
            
            if clip_tags:
                sections.append(f"AI Analysis: {', '.join(clip_tags)}")
            
            if additional_tags:
                sections.append(f"Additional: {', '.join(additional_tags)}")
            
            return ". ".join(sections) + "."
        else:
            sections = []
            
            if core_tags:
                sections.append(f"人物特征: {', '.join(core_tags)}")
            
            if variable_tags:
                sections.append(f"状态环境: {', '.join(variable_tags)}")
            
            if clip_tags:
                sections.append(f"AI分析: {', '.join(clip_tags)}")
            
            if additional_tags:
                sections.append(f"附加描述: {', '.join(additional_tags)}")
            
            return "。".join(sections) + "。"
    
    @staticmethod
    def _format_json(core_variables: Dict, variable_variables: Dict, 
                    clip_analysis: Dict, additional_tags: List[str]) -> str:
        """格式化为JSON"""
        result = {
            "metadata": {
                "generator": "ComfyUI Character Labeler",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            },
            "core_variables": core_variables,
            "variable_variables": variable_variables,
            "clip_analysis": clip_analysis if clip_analysis else {},
            "additional_tags": additional_tags,
            "summary": {
                "core_tags_count": sum(len(v) for v in core_variables.values()) if core_variables else 0,
                "variable_tags_count": sum(len(v) for v in variable_variables.values()) if variable_variables else 0,
                "clip_tags_count": len(clip_analysis) if clip_analysis else 0,
                "additional_tags_count": len(additional_tags)
            }
        }
        
        return json.dumps(result, ensure_ascii=False, indent=2)
    
    @staticmethod
    def _format_prompt(tags: List[str], language: str = "中文") -> str:
        """格式化为提示词格式"""
        # 对标签进行排序，让更重要的标签在前面
        if language == "英文":
            priority_keywords = ["1girl", "1boy", "male", "female", "portrait", "full body", "detailed"]
        else:
            priority_keywords = ["女孩", "男孩", "男性", "女性", "肖像", "全身", "详细"]
        
        # 将优先级高的标签移到前面
        sorted_tags = []
        for keyword in priority_keywords:
            for tag in tags:
                if keyword.lower() in tag.lower() and tag not in sorted_tags:
                    sorted_tags.append(tag)
        
        # 添加剩余的标签
        for tag in tags:
            if tag not in sorted_tags:
                sorted_tags.append(tag)
        
        # 确保不超过合理的长度
        if len(sorted_tags) > 20:
            sorted_tags = sorted_tags[:20]
        
        return ", ".join(sorted_tags)
    
    @staticmethod
    def create_prompt_from_labels(labels: str, style: str = "normal") -> str:
        """
        从标签创建提示词
        
        Args:
            labels: 标签字符串
            style: 风格 ("normal", "anime", "realistic", "detailed")
            
        Returns:
            提示词字符串
        """
        # 分割标签
        tag_list = [tag.strip() for tag in labels.split(",") if tag.strip()]
        
        # 根据风格添加前缀
        if style == "anime":
            prefix = "anime style, "
        elif style == "realistic":
            prefix = "photorealistic, "
        elif style == "detailed":
            prefix = "masterpiece, best quality, ultra-detailed, "
        else:
            prefix = ""
        
        # 组合提示词
        prompt = prefix + ", ".join(tag_list)
        
        # 确保长度合理
        if len(prompt) > 300:
            prompt = prompt[:300] + "..."
        
        return prompt