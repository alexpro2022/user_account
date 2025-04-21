from enum import Enum

from toolkit.models.base import Base, Mapped, mapped_column


class Role(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


# class Role(Base):
#     name: Mapped[str]
#     users: Mapped[list["User"]] = orm.relationship(back_populates="role")


class User(Base):
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_pwd: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    # disabled: Mapped[bool | None]
    role: Mapped[Role]
    # role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))  # , default=1, server_default=text("1"))
    # role: Mapped["Role"] = orm.relationship("Role", back_populates="users", lazy="joined")

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def is_admin(self) -> bool:
        return self.role == Role.ADMIN
