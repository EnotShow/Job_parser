from enum import Enum


class TemplatesPath(Enum):
    ACTIVATION = "account_activation.html"
    ADMIN_ALERT = ...
    PASSWORD_RECOVERY = "password_recovery.html"


class EmailSubject(Enum):
    ACTIVATION = "Account activation"
    ADMIN_ALERT = ...
    PASSWORD_RECOVERY = "Password recovery"
