import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Event:
    event_content: str
    event_type: str
    location: str
    date: str
    time: str
    importance: int
    present_character_ids: List[int]

@dataclass
class ShortTermMemory:
    content: str
    importance: int
    memory_type: str
    source_event: str

@dataclass
class LongTermMemory:
    content: str
    importance: int
    memory_type: str

class MemoryManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def add_event(self, world_id: int, event: Event):
        self.db.create_event(
            world_id=world_id,
            event_content=event.event_content,
            event_type=event.event_type,
            location=event.location,
            event_date=event.date,
            event_time=event.time,
            importance=event.importance,
            present_character_ids=json.dumps(event.present_character_ids)
        )
    
    def get_events(self, world_id: int) -> List[Event]:
        memories = self.db.get_events(world_id)
        return [Event(
            event_content=m.content,
            event_type=m.event_type or m.memory_type,
            location=m.location or '',
            date=m.event_date or '',
            time=m.event_time or '',
            importance=m.importance,
            present_character_ids=json.loads(m.present_character_ids) if m.present_character_ids else []
        ) for m in memories]
    
    def add_short_term_memory(self, world_id: int, character_id: int, memory: ShortTermMemory) -> int:
        result = self.db.create_short_term_memory(
            world_id=world_id,
            character_id=character_id,
            content=memory.content,
            importance=memory.importance,
            memory_type=memory.memory_type,
            source_message_ids=memory.source_event
        )
        return self.db.get_new_short_term_memory_count(world_id, character_id)
    
    def add_short_term_memories_batch(self, world_id: int, character_id: int, memories: List[ShortTermMemory]) -> int:
        for mem in memories:
            self.db.create_short_term_memory(
                world_id=world_id,
                character_id=character_id,
                content=mem.content,
                importance=mem.importance,
                memory_type=mem.memory_type,
                source_message_ids=mem.source_event
            )
        return self.db.get_new_short_term_memory_count(world_id, character_id)
    
    def get_short_term_memories(self, world_id: int, character_id: int) -> Dict[str, Any]:
        memories = self.db.get_short_term_memories(world_id, character_id)
        new_count = self.db.get_new_short_term_memory_count(world_id, character_id)
        return {
            'memories': [ShortTermMemory(
                content=m.content,
                importance=m.importance,
                memory_type=m.memory_type,
                source_event=m.source_message_ids or ''
            ) for m in memories],
            'counter': new_count
        }
    
    def clear_short_term_memories(self, world_id: int, character_id: int):
        cursor = self.db.conn.cursor()
        cursor.execute('''
            DELETE FROM memories 
            WHERE world_id = ? AND character_id = ? AND memory_category = 'short_term'
        ''', (world_id, character_id))
        self.db.conn.commit()
    
    def reset_short_term_counter(self, world_id: int, character_id: int):
        self.db.reset_short_term_memory_counter(world_id, character_id)
    
    def add_long_term_memory(self, world_id: int, character_id: int, memory: LongTermMemory):
        self.db.create_long_term_memory(
            world_id=world_id,
            character_id=character_id,
            content=memory.content,
            importance=memory.importance,
            memory_type=memory.memory_type
        )
    
    def get_long_term_memories(self, world_id: int, character_id: int) -> List[LongTermMemory]:
        memories = self.db.get_long_term_memories(world_id, character_id)
        return [LongTermMemory(
            content=m.content,
            importance=m.importance,
            memory_type=m.memory_type
        ) for m in memories]
    
    def replace_long_term_memories(self, world_id: int, character_id: int, memories: List[LongTermMemory]):
        self.db.replace_long_term_memories(world_id, character_id, [
            {'content': m.content, 'importance': m.importance, 'memory_type': m.memory_type}
            for m in memories
        ])
