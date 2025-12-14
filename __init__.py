from .nodes import (
    NODE_CLASS_MAPPINGS, 
    NODE_DISPLAY_NAME_MAPPINGS
)

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

print("\033[1;32m✅ ComfyUI Character Labeler 已加载\033[0m")
print("\033[1;36m📝 节点类别: character_labeler\033[0m")
print("\033[1;35m🚀 可用的节点:\033[0m")
for node_name in NODE_CLASS_MAPPINGS.keys():
    print(f"  - \033[1;33m{node_name}\033[0m")