# -*- coding: utf-8 -*-
import re

def fix_api_client():
    with open('api/deepseek_client.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common word fixes based on context
    word_fixes = [
        # Time/date
        ('2024秒?秒?秒?', '2024年1月1日'),
        ('8秒?', '8时'),
        ('秒?秒?秒?', '年1月1日'),
        
        # Common words ending
        ('消息秒?', '消息数'),
        ('token秒?', 'token数'),
        ('历史秒?', '历史，共'),
        ('响应秒?', '响应'),
        ('用户消息秒?', '用户消息:'),
        
        # Print statements
        ('共{len(chat_history)}秒?)', '共{len(chat_history)}条")'),
        ('{len(result)}条响应秒?)', '{len(result)}条响应")'),
        ('{len(messages)}秒?', '{len(messages)}条'),
        ('{max_tokens}")', '{max_tokens}")'),
        ('请求秒?', '请求到:'),
        ('返回token秒?', '返回token数:'),
        
        # Health/body parts
        ('健康状态秒?', '健康状态:'),
        ('臀部秒?', '臀部:'),
        ('左乳房秒?', '左乳房:'),
        ('右乳房秒?', '右乳房:'),
        ('阴道秒?', '阴道:'),
        ('阴茎秒?', '阴茎:'),
        ('睾丸秒?', '睾丸:'),
        
        # Prompts
        ('免责声明秒?', '免责声明】'),
        ('虚拟世界秒?', '虚拟世界。'),
        ('世界背景秒?', '世界背景】'),
        ('角色列表秒?', '角色列表】'),
        ('未设置秒?', '未设置}'),
        ('任务秒?', '任务】'),
        ('输出格式秒?', '输出格式】'),
        ('重要秒?', '重要】'),
        
        # Other common patterns
        ('通讯工具秒?', '通讯工具）。'),
        ('不可见的秒?', '不可见的。'),
        ('叙事可能性秒?', '叙事可能性。'),
        ('建议秒?', '建议。'),
        ('真实对话秒?', '真实对话。'),
        ('约束秒?', '约束。'),
        ('不适用于这个虚拟世界秒?', '不适用于这个虚拟世界。'),
        
        # Generic fixes
        ('秒?)', '秒")'),
        ('秒?)', '条")'),
        ('秒?}', '条}'),
        ('秒?:', '":'),
        ('秒?]', ']'),
        ('秒?"', '。"'),
        ('秒?""', '。"""'),
        ('秒?', '：'),
        ('秒?', '】'),
        ('秒?', '。'),
        ('秒?', '条'),
        ('秒?', '数'),
        ('秒?', '到'),
        ('秒?', '）'),
    ]
    
    for old, new in word_fixes:
        content = content.replace(old, new)
    
    # Fix remaining \ufffd characters with context-based replacement
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if '\ufffd' in line:
            # Context-based fixes
            if 'print' in line:
                line = line.replace('\ufffd)', '")')
                line = line.replace('\ufffd}"', '}"')
                line = line.replace('\ufffd}"', '}"')
            if 'prompt' in line or '"""' in line or "'''" in line:
                line = line.replace('\ufffd', '】')
            if 'desc +=' in line:
                line = line.replace('\ufffd', '：')
            if 'return' in line:
                line = line.replace('\ufffd', '日')
                line = line.replace('日日日', '年1月1日')
            
            # Final fallback - replace with appropriate char based on position
            line = line.replace('\ufffd"', '。"')
            line = line.replace('\ufffd)', '）')
            line = line.replace('\ufffd}', '}')
            line = line.replace('\ufffd]', ']')
            line = line.replace('\ufffd:', '：')
            line = line.replace('\ufffd,', '，')
            
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Count remaining
    count = content.count('\ufffd')
    
    with open('api/deepseek_client.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

if __name__ == '__main__':
    count = fix_api_client()
    print(f'Remaining: {count}')
