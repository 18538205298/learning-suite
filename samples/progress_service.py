"""progress_service：进度业务逻辑（累加上报、按章查询）。"""

from typing import List

from sqlmodel import Session

from app.repositories.progress_repo import ProgressRepository
from app.schemas.progress import ProgressReport, ProgressResponse


class ProgressService:
    @staticmethod
    def report(session: Session, payload: ProgressReport) -> ProgressResponse:
        row = ProgressRepository.upsert(
            session,
            key=payload.key,
            ms=payload.ms,
            visits=payload.visits,
            label=payload.label,
        )
        return ProgressResponse.model_validate(row.model_dump())

    @staticmethod
    def get_by_chapter(session: Session, chapter_id: int) -> List[ProgressResponse]:
        rows = ProgressRepository.find_by_chapter(session, chapter_id)
        return [ProgressResponse.model_validate(r.model_dump()) for r in rows]
