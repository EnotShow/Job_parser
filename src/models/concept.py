# class Application(Base):
#     __tablename__ = "applications"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title = mapped_column(String(200))
#     url = mapped_column(String(200))
#
#     parent_id: Mapped[int] = mapped_column(ForeignKey("searches.id"))
#     parent: Mapped["Search"] = relationship(back_populates="children", lazy="joined")
#
#     def __repr__(self) -> str:
#         return f"Application(id={self.id!r}, title={self.title!r}"
#
#
# class Search(Base):
#     __tablename__ = "searches"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title = mapped_column(String(200))
#     url = mapped_column(String(200))
#     cv = mapped_column(String(200))
#
#     applications: Mapped[List["Application"]] = relationship(back_populates="search", lazy="lazy")
#
#     def __repr__(self) -> str:
#         return f"Searches(id={self.id!r}, title={self.title!r})"

