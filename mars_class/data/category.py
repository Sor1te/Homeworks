import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase

association_table = sqlalchemy.Table(
    'association',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('job', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('job.id')),
    sqlalchemy.Column('department', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('department.id'))
)


class Department(SqlAlchemyBase):
    __tablename__ = 'department'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    chief = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    members = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    user = sqlalchemy.orm.relationship('User')

