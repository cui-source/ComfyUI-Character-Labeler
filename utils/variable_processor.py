"""
变量处理器工具模块
"""

import json
import os
from typing import Dict, List, Any, Optional

class VariableProcessor:
    """变量处理器"""
    
    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "configs")
        self.config_dir = config_dir
        os.makedirs(self.config_dir, exist_ok=True)
        self._ensure_config_files()
    
    def _ensure_config_files(self):
        """确保配置文件存在"""
        # 核心变量配置文件路径
        core_config_path = os.path.join(self.config_dir, "core_variables.json")
        # 可变变量配置文件路径
        var_config_path = os.path.join(self.config_dir, "variable_variables.json")
        
        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(core_config_path):
            self._create_default_core_config()
        
        if not os.path.exists(var_config_path):
            self._create_default_variable_config()
    
    def _create_default_core_config(self):
        """创建默认核心变量配置"""
        default_config = {
            "appearance": {
                "hair_style": ["长发", "短发", "中长发", "卷发", "直发", "马尾", "双马尾", "丸子头", "公主切", "波波头"],
                "hair_color": ["黑色", "棕色", "金色", "银色", "红色", "蓝色", "绿色", "紫色", "粉色", "白色", "渐变", "挑染"],
                "eye_color": ["黑色", "棕色", "蓝色", "绿色", "灰色", "金色", "红色", "异色瞳"],
                "skin_tone": ["白皙", "小麦色", "古铜色", "苍白", "红润", "偏黄"],
                "body_type": ["苗条", "标准", "丰满", "健美", "娇小", "高挑"],
                "age_range": ["幼年", "少年", "青年", "成年", "中年", "老年"]
            },
            "characteristics": {
                "gender": ["男性", "女性", "中性", "其他"],
                "race": ["亚洲人", "欧洲人", "非洲人", "混血", "幻想种族"],
                "species": ["人类", "精灵", "兽人", "机械", "天使", "恶魔", "其他"]
            }
        }
        
        config_path = os.path.join(self.config_dir, "core_variables.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print(f"✅ 已创建默认核心变量配置文件: {config_path}")
    
    def _create_default_variable_config(self):
        """创建默认可变变量配置"""
        default_config = {
            "state_action": {
                "expression": {
                    "一级": ["微笑", "愤怒", "悲伤", "惊讶", "平静", "害羞", "严肃", "调皮"],
                    "二级": {
                        "微笑": ["微笑", "大笑", "偷笑", "假笑", "苦笑"],
                        "愤怒": ["愤怒", "暴怒", "不悦", "轻蔑", "烦躁"],
                        "悲伤": ["悲伤", "哭泣", "忧郁", "绝望", "寂寞"]
                    }
                },
                "pose": {
                    "一级": ["站立", "坐姿", "卧姿", "跪姿", "跳跃", "奔跑"],
                    "二级": {
                        "站立": ["正面站立", "侧面站立", "背对", "倚靠", "叉腰"],
                        "坐姿": ["正坐", "侧坐", "盘腿", "跪坐", "懒散坐"]
                    }
                },
                "action": {
                    "一级": ["瞄准", "格挡", "交谈", "施法", "演奏", "战斗", "工作", "休息"],
                    "二级": {
                        "瞄准": ["弓箭瞄准", "枪械瞄准", "魔法瞄准", "望远镜观察"],
                        "格挡": ["盾牌格挡", "武器格挡", "魔法护盾", "闪避"]
                    }
                }
            },
            "environment": {
                "background": {
                    "一级": ["城市", "荒野", "太空", "室内", "水下", "天空", "森林", "沙漠"],
                    "二级": {
                        "城市": ["现代都市", "古城", "未来城市", "贫民窟", "商业区"],
                        "荒野": ["草原", "山地", "废墟", "沼泽", "火山"]
                    }
                },
                "time": {
                    "一级": ["白天", "夜晚", "黄昏", "黎明", "午夜"],
                    "二级": {
                        "白天": ["清晨", "正午", "午后", "傍晚"],
                        "夜晚": ["深夜", "月夜", "星夜", "雨夜"]
                    }
                },
                "lighting": {
                    "一级": ["强光", "柔和光", "伦勃朗光", "逆光", "侧光", "顶光", "背光", "自然光"],
                    "二级": {
                        "强光": ["日光直射", "聚光灯", "闪光灯", "激光"],
                        "柔和光": ["阴天光", "窗光", "柔光灯", "烛光"]
                    }
                }
            },
            "style_material": {
                "art_style": {
                    "一级": ["动漫", "写实", "油画", "水彩", "像素", "卡通", "水墨", "赛博朋克"],
                    "二级": {
                        "动漫": ["日系动漫", "美式卡通", "中国风", "蒸汽波", "赛璐璐"],
                        "写实": ["超级写实", "照片写实", "半写实", "印象派写实"]
                    }
                },
                "material": {
                    "一级": ["金属", "布料", "毛绒", "皮肤", "玻璃", "塑料", "皮革", "丝绸"],
                    "二级": {
                        "金属": ["钢铁", "黄金", "白银", "青铜", "生锈金属"],
                        "布料": ["棉布", "麻布", "绒布", "丝绸", "牛仔布"]
                    }
                }
            },
            "additional": {
                "weather": ["晴天", "雨天", "雪天", "雾天", "雷电", "彩虹", "沙尘暴"],
                "season": ["春季", "夏季", "秋季", "冬季"],
                "perspective": ["平视", "俯视", "仰视", "鸟瞰", "虫视", "透视"],
                "focus": ["特写", "半身", "全身", "远景", "中景"]
            }
        }
        
        config_path = os.path.join(self.config_dir, "variable_variables.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        print(f"✅ 已创建默认可变变量配置文件: {config_path}")
    
    def load_core_variables(self) -> Dict:
        """加载核心变量配置"""
        return self._load_json_file("core_variables.json")
    
    def load_variable_variables(self) -> Dict:
        """加载可变变量配置"""
        return self._load_json_file("variable_variables.json")
    
    def _load_json_file(self, filename: str) -> Dict:
        """加载JSON文件"""
        filepath = os.path.join(self.config_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载配置文件 {filename} 失败: {e}")
            # 如果是核心变量文件，返回默认配置
            if filename == "core_variables.json":
                return self._get_default_core_config()
            else:
                return self._get_default_variable_config()
    
    def _get_default_core_config(self) -> Dict:
        """获取默认核心变量配置（不写入文件）"""
        return {
            "appearance": {
                "hair_style": ["长发", "短发", "中长发", "卷发", "直发", "马尾", "双马尾", "丸子头", "公主切", "波波头"],
                "hair_color": ["黑色", "棕色", "金色", "银色", "红色", "蓝色", "绿色", "紫色", "粉色", "白色", "渐变", "挑染"],
                "eye_color": ["黑色", "棕色", "蓝色", "绿色", "灰色", "金色", "红色", "异色瞳"],
                "skin_tone": ["白皙", "小麦色", "古铜色", "苍白", "红润", "偏黄"],
                "body_type": ["苗条", "标准", "丰满", "健美", "娇小", "高挑"],
                "age_range": ["幼年", "少年", "青年", "成年", "中年", "老年"]
            },
            "characteristics": {
                "gender": ["男性", "女性", "中性", "其他"],
                "race": ["亚洲人", "欧洲人", "非洲人", "混血", "幻想种族"],
                "species": ["人类", "精灵", "兽人", "机械", "天使", "恶魔", "其他"]
            }
        }
    
    def _get_default_variable_config(self) -> Dict:
        """获取默认可变变量配置（不写入文件）"""
        return {
            "state_action": {
                "expression": {
                    "一级": ["微笑", "愤怒", "悲伤", "惊讶", "平静", "害羞", "严肃", "调皮"],
                    "二级": {
                        "微笑": ["微笑", "大笑", "偷笑", "假笑", "苦笑"],
                        "愤怒": ["愤怒", "暴怒", "不悦", "轻蔑", "烦躁"],
                        "悲伤": ["悲伤", "哭泣", "忧郁", "绝望", "寂寞"]
                    }
                },
                "pose": {
                    "一级": ["站立", "坐姿", "卧姿", "跪姿", "跳跃", "奔跑"],
                    "二级": {
                        "站立": ["正面站立", "侧面站立", "背对", "倚靠", "叉腰"],
                        "坐姿": ["正坐", "侧坐", "盘腿", "跪坐", "懒散坐"]
                    }
                },
                "action": {
                    "一级": ["瞄准", "格挡", "交谈", "施法", "演奏", "战斗", "工作", "休息"],
                    "二级": {
                        "瞄准": ["弓箭瞄准", "枪械瞄准", "魔法瞄准", "望远镜观察"],
                        "格挡": ["盾牌格挡", "武器格挡", "魔法护盾", "闪避"]
                    }
                }
            },
            "environment": {
                "background": {
                    "一级": ["城市", "荒野", "太空", "室内", "水下", "天空", "森林", "沙漠"],
                    "二级": {
                        "城市": ["现代都市", "古城", "未来城市", "贫民窟", "商业区"],
                        "荒野": ["草原", "山地", "废墟", "沼泽", "火山"]
                    }
                },
                "time": {
                    "一级": ["白天", "夜晚", "黄昏", "黎明", "午夜"],
                    "二级": {
                        "白天": ["清晨", "正午", "午后", "傍晚"],
                        "夜晚": ["深夜", "月夜", "星夜", "雨夜"]
                    }
                },
                "lighting": {
                    "一级": ["强光", "柔和光", "伦勃朗光", "逆光", "侧光", "顶光", "背光", "自然光"],
                    "二级": {
                        "强光": ["日光直射", "聚光灯", "闪光灯", "激光"],
                        "柔和光": ["阴天光", "窗光", "柔光灯", "烛光"]
                    }
                }
            },
            "style_material": {
                "art_style": {
                    "一级": ["动漫", "写实", "油画", "水彩", "像素", "卡通", "水墨", "赛博朋克"],
                    "二级": {
                        "动漫": ["日系动漫", "美式卡通", "中国风", "蒸汽波", "赛璐璐"],
                        "写实": ["超级写实", "照片写实", "半写实", "印象派写实"]
                    }
                },
                "material": {
                    "一级": ["金属", "布料", "毛绒", "皮肤", "玻璃", "塑料", "皮革", "丝绸"],
                    "二级": {
                        "金属": ["钢铁", "黄金", "白银", "青铜", "生锈金属"],
                        "布料": ["棉布", "麻布", "绒布", "丝绸", "牛仔布"]
                    }
                }
            },
            "additional": {
                "weather": ["晴天", "雨天", "雪天", "雾天", "雷电", "彩虹", "沙尘暴"],
                "season": ["春季", "夏季", "秋季", "冬季"],
                "perspective": ["平视", "俯视", "仰视", "鸟瞰", "虫视", "透视"],
                "focus": ["特写", "半身", "全身", "远景", "中景"]
            }
        }
    
    def get_variable_options(self, variable_type: str, category: str = None, subcategory: str = None) -> Any:
        """
        获取变量选项
        
        Args:
            variable_type: "core" 或 "variable"
            category: 类别名称
            subcategory: 子类别名称
            
        Returns:
            变量选项
        """
        if variable_type == "core":
            data = self.load_core_variables()
        else:
            data = self.load_variable_variables()
        
        if category is None:
            return data
        
        if category in data:
            category_data = data[category]
            if subcategory is None:
                return category_data
            
            if subcategory in category_data:
                return category_data[subcategory]
        
        return None
    
    def validate_variable_selection(self, selections: Dict, variable_type: str) -> Dict:
        """验证变量选择"""
        if variable_type == "core":
            template = self.load_core_variables()
        else:
            template = self.load_variable_variables()
        
        validated = {}
        
        for category, category_selections in selections.items():
            if category in template:
                validated[category] = {}
                
                if variable_type == "core":
                    # 核心变量的验证
                    for var_name, value in category_selections.items():
                        if var_name in template[category]:
                            options = template[category][var_name]
                            if isinstance(options, list) and value in options:
                                validated[category][var_name] = value
                else:
                    # 可变变量的验证
                    for var_name, levels in category_selections.items():
                        if var_name in template[category]:
                            template_levels = template[category][var_name]
                            if isinstance(template_levels, dict) and "一级" in template_levels:
                                validated_levels = {"一级": "", "二级": ""}
                                
                                # 验证一级选项
                                level1_value = levels.get("一级", "")
                                if level1_value in template_levels["一级"]:
                                    validated_levels["一级"] = level1_value
                                
                                # 验证二级选项
                                level2_value = levels.get("二级", "")
                                if level2_value and "二级" in template_levels:
                                    level2_options = template_levels["二级"].get(level1_value, [])
                                    if level2_value in level2_options:
                                        validated_levels["二级"] = level2_value
                                
                                validated[category][var_name] = validated_levels
        
        return validated


# 创建全局实例
variable_processor = VariableProcessor()