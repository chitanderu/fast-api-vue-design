from datetime import datetime
from sqlalchemy import BigInteger, Column, DateTime, String, Text
from config.database import Base
from config.env import DataBaseConfig
from utils.common_util import SqlalchemyUtil


class SysUserNote(Base):
    """
    用户个人笔记表
    """

    __tablename__ = 'sys_user_note'
    __table_args__ = {'comment': '用户个人笔记表'}

    note_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='笔记ID')
    user_id = Column(BigInteger, nullable=False, comment='用户ID')
    content = Column(Text, nullable=False, comment='笔记内容')
    del_flag = Column(String(1), nullable=True, server_default='0', comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(
        String(64),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='创建者',
    )
    create_time = Column(DateTime, nullable=True, comment='创建时间', default=datetime.now())
    update_by = Column(
        String(64),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='更新者',
    )
    update_time = Column(DateTime, nullable=True, comment='更新时间', default=datetime.now())
    remark = Column(
        String(500),
        nullable=True,
        server_default=SqlalchemyUtil.get_server_default_null(DataBaseConfig.db_type),
        comment='备注',
    )
