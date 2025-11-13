import reflex as rx
from app.states.auth_state import AuthState

from app.pages.dashboards import (
    admin_dashboard,
    user_admin_dashboard,
    tecnico_dashboard,
)


@rx.page(route="/redxtire", on_load=AuthState.require_login)
def redxtire_page() -> rx.Component:
    return rx.box(
        rx.match(
            AuthState.user_role,
            ("Administrador", admin_dashboard()),
            ("Usuario Administrador", user_admin_dashboard()),
            ("Usuario Técnico", tecnico_dashboard()),
        )
    )