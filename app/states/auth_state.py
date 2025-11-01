import reflex as rx
import httpx
from typing import TypedDict, Literal
import hashlib
import logging
from app.database.config import get_db, get_tenant_db
from app.database.models import Usuario, Cliente
from sqlalchemy.orm import Session

BASE_API_URL = "tu_url_api_aqui"
Role = Literal["Administrador", "Usuario Administrador", "Usuario Técnico"]


class User(TypedDict):
    username: str
    password_hash: str
    role: Role
    client_id: int
    schema_name: str


class AuthState(rx.State):
    error_message: str = ""
    is_authenticated: bool = False
    current_user: User | None = None

    def _get_user_from_db(self, username: str):
        """Find a user across all active tenant schemas."""
        try:
            with get_db() as db:
                all_clients = db.query(Cliente).filter(Cliente.activo == True).all()
                for client in all_clients:
                    with get_tenant_db(client.schema_name) as tenant_db:
                        user = (
                            tenant_db.query(Usuario)
                            .filter(
                                Usuario.username == username, Usuario.activo == True
                            )
                            .first()
                        )
                        if user:
                            return (user, client)
        except Exception as e:
            logging.exception(f"Database error while fetching user: {e}")
            self.error_message = "Error de base de datos. Contacte al administrador."
        return (None, None)

    @rx.event
    def login(self, form_data: dict):
        self.error_message = ""
        username = form_data.get("username", "").strip().lower()
        password = form_data.get("password", "").strip()
        if not username or not password:
            self.error_message = "Username y password son requeridos."
            return
        db_user, client = self._get_user_from_db(username)
        if not db_user or not client:
            self.error_message = "Inválido el username o password."
            return
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if password_hash != db_user.password_hash:
            self.error_message = "Inválido el password o username."
            return
        self.is_authenticated = True
        self.current_user = {
            "username": db_user.username,
            "password_hash": db_user.password_hash,
            "role": db_user.role,
            "client_id": client.id,
            "schema_name": client.schema_name,
        }
        return rx.redirect("/redxtire")

    @rx.event
    async def register(self, form_data: dict):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BASE_API_URL}/register", json=form_data)
            if response.status_code == 201:
                return rx.redirect("/login")
            else:
                self.error_message = "El registro falló. Por favor intenta nuevamente."
        except Exception as e:
            logging.exception(f"Error during registration: {e}")
            self.error_message = "Ocurrió un error. Por favor intenta nuevamente."

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.current_user = None
        self.error_message = ""
        return rx.redirect("/")

    @rx.var
    def current_user_role(self) -> str:
        if self.current_user:
            return self.current_user.get("role", "")
        return ""

    @rx.var
    def client_schema(self) -> str:
        if self.current_user:
            return self.current_user.get("schema_name", "public")
        return "public"

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