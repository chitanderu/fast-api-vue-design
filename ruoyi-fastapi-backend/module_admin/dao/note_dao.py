from datetime import datetime
from sqlalchemy import Select, and_, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from module_admin.entity.do.note_do import SysUserNote
from module_admin.entity.vo.note_vo import NotePageQueryModel
from utils.page_util import PageUtil


class NoteDao:
    @classmethod
    async def get_user_note_page(cls, db: AsyncSession, user_id: int, query: NotePageQueryModel):
        base_query: Select = select(SysUserNote).where(
            and_(SysUserNote.user_id == user_id, SysUserNote.del_flag == '0')
        ).order_by(SysUserNote.create_time.desc())
        return await PageUtil.paginate(db, base_query, query.page_num, query.page_size, is_page=True)

    @classmethod
    async def get_user_note(cls, db: AsyncSession, note_id: int, user_id: int) -> Optional[SysUserNote]:
        result = await db.execute(
            select(SysUserNote).where(
                and_(SysUserNote.note_id == note_id, SysUserNote.user_id == user_id, SysUserNote.del_flag == '0')
            )
        )
        return result.scalars().first()

    @classmethod
    async def add_note(cls, db: AsyncSession, note: SysUserNote):
        db.add(note)
        await db.flush()
        await db.refresh(note)
        return note

    @classmethod
    async def update_note_content(cls, db: AsyncSession, note_id: int, user_id: int, content: str):
        await db.execute(
            update(SysUserNote)
            .where(and_(SysUserNote.note_id == note_id, SysUserNote.user_id == user_id, SysUserNote.del_flag == '0'))
            .values(content=content, update_time=datetime.now())
        )

    @classmethod
    async def delete_notes(cls, db: AsyncSession, note_ids: List[int], user_id: int):
        await db.execute(
            update(SysUserNote)
            .where(and_(SysUserNote.note_id.in_(note_ids), SysUserNote.user_id == user_id, SysUserNote.del_flag == '0'))
            .values(del_flag='2', update_time=datetime.now())
        )

    @classmethod
    async def count_notes(cls, db: AsyncSession, note_ids: List[int], user_id: int) -> int:
        result = await db.execute(
            select(func.count()).select_from(SysUserNote).where(
                and_(SysUserNote.note_id.in_(note_ids), SysUserNote.user_id == user_id, SysUserNote.del_flag == '0')
            )
        )
        return result.scalar()
