# -*- coding: utf-8 -*-
import os

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    replacements = [
        ('秒")', '秒")'),
        ('秒", f"', '秒", f"'),
        ('秒", "', '秒", "'),
        ('错误: {e})', '错误: {e})'),
        ('错误: {e}"', '错误: {e}"'),
        ('秒', '秒'),
        ('错误', '错误'),
        ('时间', '时间'),
        ('消息', '消息'),
        ('模式', '模式'),
        ('事件', '事件'),
        ('日', '日'),
        ('日"', '日"'),
        ('日")', '日")'),
        ('日]', '日]'),
        ('日,', '日,'),
        ('年1月', '年1月'),
        ('8时', '8时'),
        ('列表', '列表'),
        ('标记', '标记'),
        ('触发', '触发'),
        ('存储', '存储'),
        ('完成', '完成'),
        ('数量', '数量'),
        ('条 {len', '条 {len'),
        ('条 {event', '条 {event'),
        ('重要性', '重要性'),
        ('跳过', '跳过'),
        ('角色', '角色'),
        ('计数器', '计数器'),
        ('记忆', '记忆'),
        ('判断', '判断'),
        ('篇章', '篇章'),
        ('内容', '内容'),
        ('下一个', '下一个'),
        ('失败', '失败'),
        ('帮助', '帮助'),
        ('交流', '交流'),
        ('更新', '更新'),
        ('操作', '操作'),
        ('数据', '数据'),
        (': {world.user_message_count}', ': {world.user_message_count}'),
        ('说话', '说话'),
        ('活跃度', '活跃度'),
        ('超时', '超时'),
        ('推进到', '推进到'),
    ]
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {filepath}')
    else:
        print(f'No changes: {filepath}')

if __name__ == '__main__':
    files = [
        'core/dialogue_manager.py',
        'core/event_extractor.py',
        'core/long_term_memory_summarizer.py',
        'core/memory_system.py',
        'api/deepseek_client.py',
    ]
    
    for f in files:
        if os.path.exists(f):
            fix_file(f)
