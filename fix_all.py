# -*- coding: utf-8 -*-
import re

def fix_all():
    with open('core/dialogue_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix all remaining corrupted characters
    # Pattern: context-based replacement
    
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if '\ufffd' in line:
            # Fix specific patterns
            # Line 285: role list
            line = line.replace('角色列表?', '角色列表')
            line = line.replace('角色列表?', '角色列表')
            
            # Line 288-289: regex patterns
            line = line.replace('秒?([^】]+)秒?', '【-([^】]+)】')
            line = line.replace('秒?[^】]+)秒?', '【([^】]+)】')
            line = line.replace('结束通讯秒?', '结束通讯）')
            line = line.replace('开始通讯秒?', '开始通讯）')
            line = line.replace('秒?角色名】', '【-角色名】')
            
            # Line 294-298: markers
            line = line.replace('标记?', '标记）')
            line = line.replace('标记忆?', '标记）')
            line = line.replace('秒?开头的', '【-开头的')
            
            # Line 311: filter
            line = line.replace('秒?角色名】标记?', '【-角色名】标记）')
            line = line.replace('秒??[^】]+秒?', '【-?[^】]+】')
            
            # Line 368: message range
            line = line.replace('第{len(user_messages)}秒?)', '第{len(user_messages)}条")')
            
            # Line 384: time advancement
            line = line.replace('秒}秒?)', '秒}秒")')
            
            # Line 430, 462: skip event
            line = line.replace('跳过事件提秒?)', '跳过事件提取")')
            
            # Line 465: dialogue count
            line = line.replace('}秒?)', '条")')
            
            # Line 581-592: prompt
            line = line.replace('篇章秒?', '篇章。')
            line = line.replace('篇章秒?', '篇章：')
            line = line.replace('内容秒?', '内容：')
            line = line.replace('条）秒?', '条）：')
            line = line.replace('False秒?', 'False。')
            line = line.replace('内容秒?""', '内容。"""')
            
            # Line 681: memory summary
            line = line.replace('秒?{len(new_memories)}', '有{len(new_memories)}')
            
            # Line 737: type info
            line = line.replace('秒? {world.user_message_count}', ': {world.user_message_count}')
            
            # Line 792: communication role
            line = line.replace('}秒?)', '}条")')
            
            # Line 800: no available role
            line = line.replace('通讯工具秒?)', '通讯工具）')
            
            # Line 824, 1412: history messages
            line = line.replace('}秒?)', '条")')
            
            # Line 903: API1 role list
            line = line.replace('同一位置秒?', '同一位置）')
            
            # Line 986: API1 response
            line = line.replace('个响秒?)', '个响应")')
            
            # Line 1070: remove actions
            line = line.replace('所有动秒?)', '所有动作")')
            
            # Line 1199: trigger event
            line = line.replace('事件提秒?.."', '事件提取..."')
            
            # Line 1682: advance time
            line = line.replace('}秒?)', '}秒")')
            
            # Line 1688: time advanced
            line = line.replace('时间秒?', '时间从')
            line = line.replace('推进到秒?', '推进到：')
            
            # Generic fixes
            line = line.replace('秒?)', '秒")')
            line = line.replace('秒?)', '条")')
            line = line.replace('秒?""', '。"""')
            line = line.replace('秒?', '）')
            line = line.replace('秒?', '：')
            line = line.replace('秒?', '。')
            line = line.replace('秒?', '条')
            line = line.replace('秒?', '有')
            
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Count remaining
    count = content.count('\ufffd')
    
    with open('core/dialogue_manager.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

if __name__ == '__main__':
    count = fix_all()
    print(f'Remaining: {count}')
