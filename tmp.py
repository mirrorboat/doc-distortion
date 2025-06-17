import re

def extract_and_join(text):
    # 定义正则表达式，匹配<|md_start|>和<|md_end|>之间的内容
    pattern = r'<\|md_start\|>(.*?)<\|md_end\|>'
    
    # 使用 re.findall 提取所有匹配的内容
    matches = re.findall(pattern, text, re.DOTALL)
    
    # 将提取的内容用 '\n\n' 拼接
    result = '\n\n'.join(matches)
    
    return result

# 示例字符串
text = """
一些文本<|md_start|>第一段内容<|md_end|>更多文本
另一些文本<|md_start|>第二段内容<|md_end|>结束
"""

# 调用函数并打印结果
output = extract_and_join(text)
print(output)