import json
import os
from functools import lru_cache

from anthropic import Anthropic
from anthropic.types import Message


class AnthropicProcessor:
    def __init__(self) -> None:
        self.client: Anthropic = Anthropic(
            api_key=os.environ['CLAUDE_API_KEY'],
        )

    @lru_cache(maxsize=32)
    async def get_answer_of_claude(self, prompt: str) -> str:
        message: Message = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=1000,
            temperature=0.0,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return json.loads(message.model_dump_json())["content"][0]["text"]
