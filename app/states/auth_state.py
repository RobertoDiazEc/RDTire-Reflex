import reflex as rx
from typing import TypedDict, Literal
import hashlib
import logging

Role = Literal["Administrador", "Usuario Administrador", "Usuario Técnico"]


class User(TypedDict):
    username: str
    password_hash: str
    role: Role


USERS_DB: list[User] = [
    {
        "username": "admin",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Administrador",
    },
    {
        "username": "useradmin",
        "password_hash": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Usuario Administrador",
    },
    {
        "username": "tecnico",
        "password_hash": hashlib.sha256("tecnico123".encode()).hexdigest(),
        "role": "Usuario Técnico",
    },
]


class AuthState(rx.State):
    error_message: str = ""
    is_authenticated: bool = False
    current_user: User | None = None

    def _get_user(self, username: str) -> User | None:
        return next((user for user in USERS_DB if user["username"] == username), None)

    @rx.event
    def login(self, form_data: dict[str, str]):
        self.error_message = ""
        username = form_data.get("username", "").strip()
        password = form_data.get("password", "").strip()
        if not username or not password:
            self.error_message = "Username and password are required."
            return
        user = self._get_user(username)
        if not user:
            self.error_message = "Invalid username or password."
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != user["password_hash"]:
            self.error_message = "Invalid username or password."
            return
        self.is_authenticated = True
        self.current_user = user
        return rx.redirect("/")

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.current_user = None
        self.error_message = ""
        return rx.redirect("/login")

    @rx.var
    def current_user_role(self) -> str:
        if self.current_user:
            return self.current_user.get("role", "")
        return ""

    @rx.event
    def require_login(self) -> rx.event.EventSpec | None:
        if not self.is_authenticated:
            return rx.redirect("/login")
        return None

    @rx.event
    def require_role(self, required_roles: list[Role]) -> rx.event.EventSpec | None:
        if not self.is_authenticated:
            return rx.redirect("/login")
        if self.current_user and self.current_user["role"] not in required_roles:
            logging.warning(
                f"User {self.current_user['username']} with role {self.current_user['role']} tried to access a page requiring one of {required_roles}"
            )
            return rx.redirect("/")
        return None