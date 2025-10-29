import reflex as rx
import httpx
from typing import TypedDict, Literal
import hashlib
import logging

BASE_API_URL = "tu_url_api_aqui"  # Reemplaza con tu URL de API real

Role = Literal[
    "Administrador", 
    "Usuario Administrador", 
    "Usuario Técnico"]


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
            self.error_message = "Username y password son requeridos."
            return
        user = self._get_user(username)
        if not user:
            self.error_message = "Invalido el username o password."
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != user["password_hash"]:
            self.error_message = "Invalido el password o username."
            return
        self.is_authenticated = True
        self.current_user = user
        return rx.redirect("/")
    
    @rx.event
    async def register(self, form_data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BASE_API_URL}/register", json=form_data)
                
            if response.status_code == 201:
                # Manejar registro exitoso
                return rx.redirect("/login")
            else:
                self.error_message = "El registro falló. Por favor intenta nuevamente."
        except Exception as e:
            self.error_message = "Ocurrió un error. Por favor intenta nuevamente."

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