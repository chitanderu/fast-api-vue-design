from fastapi import APIRouter, Depends, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.get_db import get_db
from module_admin.entity.vo.note_vo import AddNoteModel, DeleteNoteModel, EditNoteModel, NotePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.note_service import NoteService
from utils.response_util import ResponseUtil


noteController = APIRouter(prefix='/system/note', dependencies=[Depends(LoginService.get_current_user)])


@noteController.get('/list')
async def get_note_list(
    request: Request,
    note_query: NotePageQueryModel = Depends(NotePageQueryModel.as_query),
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    note_page = await NoteService.get_note_page_services(query_db, note_query, current_user)
    return ResponseUtil.success(model_content=note_page)


@noteController.post('')
@ValidateFields(validate_model='add_note')
async def add_note(
    request: Request,
    add_model: AddNoteModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    await NoteService.add_note_services(query_db, add_model, current_user)
    return ResponseUtil.success(msg='新增成功')


@noteController.put('')
@ValidateFields(validate_model='edit_note')
async def edit_note(
    request: Request,
    edit_model: EditNoteModel,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    await NoteService.edit_note_services(query_db, edit_model, current_user)
    return ResponseUtil.success(msg='修改成功')


@noteController.delete('/{note_ids}')
async def delete_note(
    request: Request,
    note_ids: str,
    query_db: AsyncSession = Depends(get_db),
    current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    await NoteService.delete_note_services(query_db, DeleteNoteModel(noteIds=note_ids), current_user)
    return ResponseUtil.success(msg='删除成功')
