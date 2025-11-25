from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size
from module_admin.annotation.pydantic_annotation import as_query


class NoteModel(BaseModel):
    """
    用户笔记模型
    """

    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    note_id: Optional[int] = Field(default=None, description='笔记ID')
    content: Optional[str] = Field(default=None, description='笔记内容')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')


class AddNoteModel(NoteModel):
    @NotBlank(field_name='content', message='笔记内容不能为空')
    @Size(field_name='content', min_length=1, max_length=2000, message='笔记内容长度需在1-2000字符之间')
    def get_content(self):
        return self.content

    def validate_fields(self):
        self.get_content()

    def add_note(self):
        self.validate_fields()


class EditNoteModel(AddNoteModel):
    note_id: int = Field(description='笔记ID')

    def edit_note(self):
        self.validate_fields()


@as_query
class NotePageQueryModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteNoteModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    note_ids: str = Field(description='需要删除的笔记ID列表，多个以逗号分隔')
