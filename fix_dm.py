# -*- coding: utf-8 -*-
import re

def fix_dialogue_manager():
    with open('core/dialogue_manager.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix corrupted characters based on context
    # The replacement character is \ufffd
    
    lines = content.split('\n')
    fixed_lines = []
    
    for line in lines:
        if '\ufffd' in line:
            # Fix based on context
            # Time/date patterns
            line = line.replace('{day}\ufffd", f"{hour}\ufffd', '{day}日", f"{hour}时"')
            line = line.replace('\ufffd"', '日"')
            line = line.replace('\ufffd)"', '日")')
            line = line.replace('\ufffd]', '日]')
            line = line.replace('\ufffd,', '日,')
            line = line.replace('8\ufffd', '8时')
            line = line.replace('2024\ufffd\ufffd\ufffd', '2024年1月1日')
            
            # Print statements with time
            line = line.replace('耗时: {db_save_time:.3f}\ufffd)', '耗时: {db_save_time:.3f}秒")')
            line = line.replace('耗时: {bg_query_time:.3f}\ufffd)', '耗时: {bg_query_time:.3f}秒")')
            line = line.replace('耗时: {world_update_time:.3f}\ufffd)', '耗时: {world_update_time:.3f}秒")')
            line = line.replace('耗时: {char_update_time:.3f}\ufffd)', '耗时: {char_update_time:.3f}秒")')
            line = line.replace('耗时: {process_response_time:.3f}\ufffd)', '耗时: {process_response_time:.3f}秒")')
            line = line.replace('耗时: {total_time:.3f}\ufffd)', '耗时: {total_time:.3f}秒")')
            
            # Error messages
            line = line.replace('发生错\ufffd: {e}', '发生错误: {e}')
            line = line.replace('发生错\ufffd"', '发生错误: "')
            
            # Common words - context based
            if '时\ufffd' in line:
                line = line.replace('时\ufffd', '时间')
            if '消\ufffd' in line:
                line = line.replace('消\ufffd', '消息')
            if '模\ufffd' in line:
                line = line.replace('模\ufffd', '模式')
            if '事\ufffd' in line:
                line = line.replace('事\ufffd', '事件')
            if '列\ufffd' in line:
                line = line.replace('列\ufffd', '列表')
            if '标\ufffd' in line:
                line = line.replace('标\ufffd', '标记')
            if '触\ufffd' in line:
                line = line.replace('触\ufffd', '触发')
            if '存\ufffd' in line:
                line = line.replace('存\ufffd', '存储')
            if '完\ufffd' in line:
                line = line.replace('完\ufffd', '完成')
            if '数\ufffd' in line and '数据' not in line:
                line = line.replace('数\ufffd', '数量')
            if '重要\ufffd' in line:
                line = line.replace('重要\ufffd', '重要性')
            if '跳\ufffd' in line:
                line = line.replace('跳\ufffd', '跳过')
            if '角\ufffd' in line:
                line = line.replace('角\ufffd', '角色')
            if '计数\ufffd' in line:
                line = line.replace('计数\ufffd', '计数器')
            if '记\ufffd' in line:
                line = line.replace('记\ufffd', '记忆')
            if '判\ufffd' in line:
                line = line.replace('判\ufffd', '判断')
            if '篇\ufffd' in line:
                line = line.replace('篇\ufffd', '篇章')
            if '内\ufffd' in line:
                line = line.replace('内\ufffd', '内容')
            if '下\ufffd' in line:
                line = line.replace('下\ufffd', '下一个')
            if '失\ufffd' in line:
                line = line.replace('失\ufffd', '失败')
            if '帮\ufffd' in line:
                line = line.replace('帮\ufffd', '帮助')
            if '交\ufffd' in line:
                line = line.replace('交\ufffd', '交流')
            if '更\ufffd' in line:
                line = line.replace('更\ufffd', '更新')
            if '操\ufffd' in line:
                line = line.replace('操\ufffd', '操作')
            if '数据\ufffd' in line:
                line = line.replace('数据\ufffd', '数据')
            if '说\ufffd' in line:
                line = line.replace('说\ufffd', '说话')
            if '活跃\ufffd' in line:
                line = line.replace('活跃\ufffd', '活跃度')
            if '超\ufffd' in line:
                line = line.replace('超\ufffd', '超时')
            if '推进\ufffd' in line:
                line = line.replace('推进\ufffd', '推进到')
            if '错\ufffd' in line:
                line = line.replace('错\ufffd', '错误')
            
            # Remaining \ufffd at end of numbers (likely 秒)
            line = re.sub(r'(\d+\.\d+)\ufffd\)', r'\1秒")', line)
            line = re.sub(r'(\d+)\ufffd\)', r'\1秒")', line)
            
            # Remaining \ufffd after specific patterns
            line = line.replace('条\ufffd', '条')
            line = line.replace('\ufffd {len', '条 {len')
            line = line.replace('\ufffd {event', '条 {event')
            line = line.replace('\ufffd {char', '条 {char')
            
        fixed_lines.append(line)
    
    content = '\n'.join(fixed_lines)
    
    # Count remaining issues
    count = content.count('\ufffd')
    
    with open('core/dialogue_manager.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

if __name__ == '__main__':
    count = fix_dialogue_manager()
    print(f'Remaining corrupted chars: {count}')
