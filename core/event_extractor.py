from typing import List, Optional
from core.memory_manager import Event
import asyncio
import json
import time

EVENT_EXTRACTION_PROMPT = """你是一个事件提取专家。请从以下对话中提取重要事件、情绪变化、关系变化和信息。
对话内容：{dialogues}

在场角色：{present_characters}

请以JSON格式返回提取结果，格式如下：
{{
    "events": [
        {{
            "content": "事件描述",
            "importance": 1-10的重要性评分,
            "type": "event/emotion/relationship/information"
        }}
    ]
}}

提取规则：
1. event类型：记录发生的具体事件（如"去了某地"、"遇到了某人"、"做了某事"），importance通常为3-7
2. emotion类型：记录角色的情绪变化（如"感到高兴"、"变得愤怒"），importance通常为2-6
3. relationship类型：记录角色间关系的变化（如"开始信任"、"产生矛盾"），importance通常为3-7
4. information类型：记录重要的信息（如"得知了某事"、"了解了某情况"），importance通常为2-5
5. importance评分：1-3为普通，4-6为重要，7-8为非常重要，9-10为关键转折点
6. 只提取真正重要的事件，忽略日常寒暄和无关紧要的内容
7. 每个事件用简洁的一句话描述

请直接返回JSON，不要包含其他内容。
"""


class EventExtractor:
    def __init__(self, api_client=None):
        self.api_client = api_client
        self.cache = {}
        self.cache_ttl = 300
        self.max_cache_size = 100

    def set_api_client(self, api_client):
        self.api_client = api_client

    def _cleanup_cache(self):
        current_time = time.time()
        keys_to_remove = []

        for key, (result, timestamp) in self.cache.items():
            if current_time - timestamp > self.cache_ttl:
                keys_to_remove.append(key)

        for key in keys_to_remove:
            del self.cache[key]

        if len(self.cache) > self.max_cache_size:
            sorted_items = sorted(
                self.cache.items(),
                key=lambda x: x[1][1]
            )
            items_to_remove = len(self.cache) - self.max_cache_size
            for key, _ in sorted_items[:items_to_remove]:
                del self.cache[key]

    async def extract_events_async(
        self,
        dialogues: List[str],
        location: str,
        date: str,
        event_time: str,
        present_characters: Optional[List[str]] = None,
        present_character_ids: Optional[List[int]] = None
    ) -> List[Event]:
        if not self.api_client:
            print("警告: API客户端未设置，无法提取事件")
            return []

        if not dialogues:
            return []

        cache_key = f"events_{'_'.join(dialogues[:3])}"
        if cache_key in self.cache:
            cached_result, timestamp = self.cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_result

        dialogue_text = "\n".join([f"- {d}" for d in dialogues])
        present_chars = ", ".join(present_characters) if present_characters else "未知"

        prompt = EVENT_EXTRACTION_PROMPT.format(
            dialogues=dialogue_text,
            present_characters=present_chars
        )

        try:
            from api import Message
            messages = [
                Message(role="system", content="你是一个专业的事件提取助手，擅长从对话中识别和提取关键事件。"),
                Message(role="user", content=prompt)
            ]

            response = await self.api_client.chat_completion(
                messages=messages,
                model="ep-m-20260305201046-cbwgl",
                temperature=0.3,
                max_tokens=1000
            )

            result_text = response.content.strip()

            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            result = json.loads(result_text)

            events = []
            for event_data in result.get("events", []):
                event = Event(
                    event_content=event_data.get("content", ""),
                    event_type=event_data.get("type", "event"),
                    location=location,
                    date=date,
                    time=event_time,
                    importance=event_data.get("importance", 5),
                    present_character_ids=present_character_ids or []
                )
                events.append(event)

            self.cache[cache_key] = (events, time.time())
            if len(self.cache) > self.max_cache_size:
                self._cleanup_cache()

            return events

        except json.JSONDecodeError as e:
            print(f"事件提取JSON解析失败: {e}")
            return []
        except Exception as e:
            print(f"事件提取失败: {e}")
            return []

    def extract_events(
        self,
        dialogues: List[str],
        location: str,
        date: str,
        event_time: str,
        present_characters: Optional[List[str]] = None,
        present_character_ids: Optional[List[int]] = None
    ) -> List[Event]:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    future = executor.submit(
                        lambda: asyncio.run(
                            self.extract_events_async(
                                dialogues=dialogues,
                                location=location,
                                date=date,
                                event_time=event_time,
                                present_characters=present_characters,
                                present_character_ids=present_character_ids
                            )
                        )
                    )
                    return future.result(timeout=60)
            else:
                return loop.run_until_complete(
                    self.extract_events_async(
                        dialogues=dialogues,
                        location=location,
                        date=date,
                        event_time=event_time,
                        present_characters=present_characters,
                        present_character_ids=present_character_ids
                    )
                )
        except RuntimeError:
            return asyncio.run(
                self.extract_events_async(
                    dialogues=dialogues,
                    location=location,
                    date=date,
                    event_time=event_time,
                    present_characters=present_characters,
                    present_character_ids=present_character_ids
                )
            )
        except Exception as e:
            print(f"事件提取同步调用失败: {e}")
            return []
