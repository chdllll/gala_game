import asyncio
from typing import List, Dict, Any, Optional
from database import DatabaseManager, World, Character, RemoteCharacterEvent
from api import DeepSeekClient, Message

class RemoteEventManager:
    def __init__(self, db_manager: DatabaseManager, api_client: DeepSeekClient):
        self.db = db_manager
        self.api_client = api_client
    
    async def check_and_process_events(self, world: World, model: str = "ep-m-20260305201046-cbwgl") -> List[Dict]:
        current_date = world.current_date or "2024年1月1日"
        current_time = world.current_time or "8时"
        
        pending_events = self.db.get_pending_remote_events(current_date, current_time)
        
        timeline_events = []
        for event in pending_events:
            timeline_events.append({
                'type': 'remote_event',
                'character_name': event.character_name,
                'event_type': event.event_type,
                'description': event.description,
                'date': event.target_date,
                'time': event.target_time
            })
            self.db.mark_remote_event_as_processed(event.id)
        
        await self._generate_events_for_remote_characters(world, model)
        
        return timeline_events
    
    async def _generate_events_for_remote_characters(self, world: World, model: str = "ep-m-20260305201046-cbwgl"):
        characters = self.db.get_characters_by_world(world.id)
        user_location = world.user_location
        
        remote_characters = [
            char for char in characters 
            if char.location != user_location
        ]
        
        for char in remote_characters:
            try:
                events = await self._generate_events_for_character(world, char, model)
                for event in events:
                    self.db.create_remote_character_event(
                        character_id=char.id,
                        character_name=char.name,
                        event_type=event['event_type'],
                        description=event['description'],
                        target_date=event['target_date'],
                        target_time=event['target_time']
                    )
            except Exception as e:
                print(f"生成角色 {char.name} 的远程事件失败: {e}")
    
    async def _generate_events_for_character(
        self, 
        world: World, 
        character: Character, 
        model: str = "ep-m-20260305201046-cbwgl"
    ) -> List[Dict]:
        prompt = f"""你是一个故事事件生成器。请为以下角色生成一些可能发生的事件。

世界背景: {world.background or '无'}
角色名称: {character.name}
角色描述: {character.description or '无'}
角色当前位置: {character.location or '未知'}
当前日期: {world.current_date or '2024年1月1日'}
当前时间: {world.current_time or '8时'}

请生成1-3个该角色可能在接下来几小时或几天内发生的事件。事件应该符合角色的性格和当前处境。

返回JSON格式:
{{
    "events": [
        {{
            "event_type": "日常活动/社交/冒险/工作/休息",
            "description": "事件描述",
            "target_date": "2024年1月1日",
            "target_time": "10时"
        }}
    ]
}}
"""
        
        try:
            messages = [
                Message(role="system", content="你是一个专业的故事事件生成器。"),
                Message(role="user", content=prompt)
            ]
            
            response = await self.api_client.chat_completion(
                messages=messages,
                model=model,
                temperature=0.8,
                max_tokens=500
            )
            
            import json
            result_text = response.content.strip()
            
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()
            
            result = json.loads(result_text)
            return result.get("events", [])
            
        except Exception as e:
            print(f"生成事件失败: {e}")
            return []
    
    def cleanup_old_events(self, days: int = 7):
        deleted_count = self.db.delete_old_remote_events(days)
        print(f"清理了{deleted_count}个旧事件")
