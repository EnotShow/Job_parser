from enum import Enum

from pydantic import FilePath


class EmailTemplate(Enum):
    ACTIVATION: FilePath = "/auth/templates/account_activation.html"
    PASSWORD_RECOVERY: FilePath = "/auth/templates/password_recovery.html"


class EmailSubject(Enum):
    ACTIVATION: FilePath = "Account activation"
    PASSWORD_RECOVERY: FilePath = "Password recovery"
