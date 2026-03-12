# -*- coding: utf-8 -*-

def fix_precise():
    with open('core/dialogue_manager.py', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    fixes = {
        287: '        - communication_characters: 通过【角色名】标记需要通讯的角色列表\n        - end_communication_characters: 通过【-角色名】标记结束通讯的角色列表\n        """\n',
        290: "        # 先匹配【-角色名】模式（结束通讯）\n        end_pattern = r'【-([^】]+)】'\n",
        291: "        # 匹配【角色名】模式（开始通讯）\n        start_pattern = r'【([^】]+)】'\n",
        302: "            # 排除【-开头的（这些是结束通讯标记）\n            if not match.startswith('-'):\n",
        313: "        # 移除【角色名】和【-角色名】标记\n        filtered_message = re.sub(r'【-?[^】]+】', '', user_message)\n",
        370: '            print(f"用户消息范围：第{len(user_messages) - len(last_7_user_messages) + 1}条到第{len(user_messages)}条")\n',
        386: '                print(f"API2过一天模式检测到时间推进：{api2_time_advancement_seconds}秒")\n',
        432: '            print("没有用户消息，跳过事件提取")\n',
        464: '            print("没有角色对话，跳过事件提取")\n',
        467: '        print(f"提取所有角色对话，共{len(all_character_dialogues)}条")\n',
        583: '            prompt = f"""你是一个剧本推进判断助手。请根据最近的短期记忆和当前篇章、下一个篇章的内容，判断是否需要进入下一个篇章。\n',
        584: "当前篇章：标题：{current_chapter['title']}\n",
        591: '最近的短期记忆（共{len(short_term_memories)}条）：{memories_text}\n',
        593: '请判断是否需要进入下一个篇章。如果当前篇章的主要目标已经完成，或者故事情节已经自然过渡到下一个篇章，则返回True；否则返回False。\n',
        594: '请只返回True或False，不要返回其他内容。"""\n',
        683: '        print(f"角色 {character_name} 有{len(new_memories)} 条新的短期记忆需要总结")\n',
        739: '        print(f"world.user_message_count 类型: {type(world.user_message_count)}, 值: {world.user_message_count}")\n',
        794: '                        print(f"添加通讯角色 {comm_char.name} 到角色列表（位置: {comm_char.location}）")\n',
        802: '            print("没有可用的角色（用户在路上且未使用通讯工具）")\n',
        826: '        print(f"获取到{len(all_chat_history)}条历史消息，选择了{len(chat_history)}条")\n',
        905: '        print(f"API1: 传输给API1的角色列表（同一位置）: {[char[\'name\'] for char in all_characters_data]}")\n',
        988: '                    print(f"API1完成，获得{len(responses)}个响应")\n',
        1072: '                print(f"角色 {character.name} 正在通过通讯工具发言，移除所有动作")\n',
        1201: '            print(f"已达到用户消息边界（第{new_user_message_count}条用户消息），触发事件提取...")\n',
        1414: '        print(f"获取到{len(all_chat_history)}条历史消息，选择了{len(chat_history)}条")\n',
        1684: '            print(f"推进时间: {time_advancement_seconds}秒")\n',
        1690: '            print(f"时间从{world.current_date} {world.current_time} 推进到：{new_date_part} {new_time_part}")\n',
    }
    
    for line_num, fixed_line in fixes.items():
        lines[line_num - 1] = fixed_line
    
    content = ''.join(lines)
    
    count = content.count('\ufffd')
    
    with open('core/dialogue_manager.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

if __name__ == '__main__':
    count = fix_precise()
    print(f'Remaining: {count}')
