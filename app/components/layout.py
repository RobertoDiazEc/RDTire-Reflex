import reflex as rx

from app.utils.constant import (
    ADMIN_NAV,
    TECNICO_NAV,
    USER_ADMIN_NAV,
    INICIO_NAV,
    ESTILO_BOTON_PRINCIPAL,
)
from app.states.auth_state import AuthState
from app.components.sidebar_rd import sidebar_redx
from app.components.footer import footer


def main_layout(child: rx.Component, *args, **kwargs) -> rx.Component:
    return rx.el.div(
        sidebar_redx(),
        rx.el.div(
            #header(),
            rx.el.main(
                child, class_name="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-6"
            ),
            
            class_name="flex flex-col flex-1 overflow-auto",
        ),
        
        class_name="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[220px_1fr]",
    )