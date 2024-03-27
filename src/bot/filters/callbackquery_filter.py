import enum

from aiogram.filters.callback_data import CallbackData


class ReplyType(enum.StrEnum):
    TITLE = "title"
    DESCRIPTION = "description"
    APPLY = "apply"


class ReplyCallback(CallbackData, prefix="reply"):
    application_id: int
    search_title: str
    type: ReplyType
