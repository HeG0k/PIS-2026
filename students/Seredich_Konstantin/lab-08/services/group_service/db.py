import os

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost:5432/groups",
)


class Base(DeclarativeBase):
    pass


class GroupRecord(Base):
    __tablename__ = "groups"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    leader_id: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String, default="FORMING")

    members: Mapped[list["MemberRecord"]] = relationship(
        back_populates="group",
        cascade="all, delete-orphan",
    )


class MemberRecord(Base):
    __tablename__ = "group_members"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id: Mapped[str] = mapped_column(String, ForeignKey("groups.id"))
    volunteer_id: Mapped[str] = mapped_column(String)

    group: Mapped["GroupRecord"] = relationship(back_populates="members")


engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)
