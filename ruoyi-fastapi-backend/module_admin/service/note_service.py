from datetime import datetime
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exception import ServiceException
from module_admin.dao.note_dao import NoteDao
from module_admin.entity.do.note_do import SysUserNote
from module_admin.entity.vo.note_vo import AddNoteModel, DeleteNoteModel, EditNoteModel, NoteModel, NotePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from utils.page_util import PageResponseModel


class NoteService:
    """
    用户个人笔记服务
    """

    @classmethod
    async def get_note_page_services(cls, db: AsyncSession, query: NotePageQueryModel, current_user: CurrentUserModel):
        page_result = await NoteDao.get_user_note_page(db, current_user.user.user_id, query)
        page_result.rows = [NoteModel.model_validate(row, from_attributes=True) for row in page_result.rows]
        return PageResponseModel(**page_result.model_dump(by_alias=True))

    @classmethod
    async def add_note_services(cls, db: AsyncSession, add_model: AddNoteModel, current_user: CurrentUserModel):
        add_model.validate_fields()
        note = SysUserNote(
            user_id=current_user.user.user_id,
            content=add_model.content,
            create_by=current_user.user.user_name,
            create_time=datetime.now(),
            update_by=current_user.user.user_name,
            update_time=datetime.now(),
        )
        await NoteDao.add_note(db, note)
        await db.commit()
        return note

    @classmethod
    async def edit_note_services(cls, db: AsyncSession, edit_model: EditNoteModel, current_user: CurrentUserModel):
        edit_model.validate_fields()
        existing_note = await NoteDao.get_user_note(db, edit_model.note_id, current_user.user.user_id)
        if not existing_note:
            raise ServiceException(message='笔记不存在或无权修改')
        await NoteDao.update_note_content(db, edit_model.note_id, current_user.user.user_id, edit_model.content)
        await db.commit()

    @classmethod
    async def delete_note_services(cls, db: AsyncSession, delete_model: DeleteNoteModel, current_user: CurrentUserModel):
        note_ids: List[int] = [int(item) for item in delete_model.note_ids.split(',') if item]
        if not note_ids:
            raise ServiceException(message='请选择要删除的笔记')
        note_count = await NoteDao.count_notes(db, note_ids, current_user.user.user_id)
        if note_count != len(note_ids):
            raise ServiceException(message='存在无权删除的笔记')
        await NoteDao.delete_notes(db, note_ids, current_user.user.user_id)
        await db.commit()
