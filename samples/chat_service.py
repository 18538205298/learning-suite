"""对话业务逻辑。不写 SQL（调 Repository）、不依赖 request。"""
import json
from typing import AsyncIterator, Optional
from sqlmodel import Session
from app.core.config import settings
from app.services.prompt_service import load_prompt
from app.repositories.history_repo import HistoryRepository
from app.providers import openai as openai_provider
from app.providers import local as local_provider


class ChatService:
    @staticmethod
    def _get_provider():
        """根据配置选择 provider 模块。默认 openai（无 key 时自动 mock）。"""
        if settings.ai_provider == "local":
            return local_provider
        return openai_provider

    @staticmethod
    def _build_messages(system: str, user_prompt: str, message: str) -> list[dict]:
        return [
            {"role": "system", "content": system + "\n\n" + user_prompt},
            {"role": "user", "content": message},
        ]

    @staticmethod
    async def chat(
        session: Session,
        message: str,
        project_id: str,
        prompt_type: str,
        pack_id: str,
        stream: bool = False,
    ) -> AsyncIterator[str]:
        """对话。流式时 yield 增量；非流式时 yield 完整回复。"""
        system, user_prompt = load_prompt(project_id, prompt_type)
        messages = ChatService._build_messages(system, user_prompt, message)
        provider = ChatService._get_provider()

        full_reply: list[str] = []

        async for chunk in provider.chat(messages, stream=stream):
            full_reply.append(chunk)
            yield chunk

        # 保存对话历史（user + assistant）
        reply_text = "".join(full_reply)
        HistoryRepository.create(
            session, role="user", content=message,
            pack_id=pack_id, project_id=project_id, mode=prompt_type,
        )
        HistoryRepository.create(
            session, role="assistant", content=reply_text,
            pack_id=pack_id, project_id=project_id, mode=prompt_type,
        )
