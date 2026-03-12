# -*- coding: utf-8 -*-
import re

def fix_deepseek_client():
    with open('api/deepseek_client.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix specific patterns based on context
    fixes = [
        # Print statements ending
        ('print(f"API调用开始，模型: {model}, 消息数: {len(messages)}, 最大token: {max_tokens}")', 
         'print(f"API调用开始，模型: {model}, 消息数: {len(messages)}, 最大token: {max_tokens}")'),
        
        ('print(f"[DEBUG] 开始发送POST请求到: {url}")',
         'print(f"[DEBUG] 开始发送POST请求到: {url}")'),
        
        ('print(f"API调用成功，返回token数: {usage.get(\'total_tokens\', \'unknown\')}")',
         'print(f"API调用成功，返回token数: {usage.get(\'total_tokens\', \'unknown\')}")'),
        
        # Date/time defaults
        ('current_date: str = "2024年1月1日"',
         'current_date: str = "2024年1月1日"'),
        ('current_time: str = "8时"',
         'current_time: str = "8时"'),
        
        # Print statements with counts
        ('print(f"构建对话历史，共{len(chat_history)}条")',
         'print(f"构建对话历史，共{len(chat_history)}条")'),
        ('print(f"发送用户消息: {user_message}")',
         'print(f"发送用户消息: {user_message}")'),
        ('print(f"解析得到{len(result)}条响应")',
         'print(f"解析得到{len(result)}条响应")'),
    ]
    
    # Apply fixes
    for old, new in fixes:
        content = content.replace(old, new)
    
    # Fix remaining corrupted characters using regex patterns
    # Pattern 1: print statements with corrupted endings
    content = re.sub(r'print\(f"([^"]*?)条"\)', r'print(f"\1条")', content)
    content = re.sub(r'print\(f"([^"]*?)秒"\)', r'print(f"\1秒")', content)
    
    # Pattern 2: Default date/time values
    content = content.replace('2024年1月1日', '2024年1月1日')
    content = content.replace('8时', '8时')
    
    # Pattern 3: Prompt endings
    content = re.sub(r'【([^】]*?)】', r'【\1】', content)
    
    # Pattern 4: Chinese punctuation
    content = content.replace('。', '。')
    content = content.replace('：', '：')
    content = content.replace('，', '，')
    content = content.replace('）', '）')
    content = content.replace('（', '（')
    
    # Count remaining corrupted chars
    count = content.count('\ufffd')
    
    with open('api/deepseek_client.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

if __name__ == '__main__':
    count = fix_deepseek_client()
    print(f'Remaining corrupted chars: {count}')
