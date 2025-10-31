import reflex as rx
from app.utils.constant import ADMIN_NAV, TECNICO_NAV, USER_ADMIN_NAV, INICIO_NAV, ESTILO_BOTON_PRINCIPAL
from app.states.auth_state import AuthState



def sidebar_item(item: dict) -> rx.Component:
    return rx.el.a(
        rx.icon(item["icon"], class_name="h-5 w-5"),
        rx.el.span(item["name"]),
        href=item["path"],
        class_name="flex items-center gap-3 rounded-lg px-3 py-2 text-gray-500 transition-all hover:text-gray-900",
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.a(
                rx.icon("circle-dot", class_name="h-6 w-6 text-emerald-600"),
                rx.el.span("RDTire-APP", class_name="font-semibold"),
                href="/redxtire",
                class_name="flex items-center gap-2 font-semibold",
            ),
            class_name="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6",
        ),
        rx.el.div(
            rx.el.nav(
                rx.match(
                    AuthState.current_user_role,
                    ("Administrador", rx.foreach(ADMIN_NAV, sidebar_item)),
                    ("Usuario Administrador", rx.foreach(USER_ADMIN_NAV, sidebar_item)),
                    ("Usuario Técnico", rx.foreach(TECNICO_NAV, sidebar_item)),
                    ("Inicio App", rx.foreach(INICIO_NAV, sidebar_item))
                ),
                class_name="flex-1 items-start px-2 text-sm font-medium lg:px-4",
            ),
            class_name="flex-1 overflow-auto py-2",
        ),
        class_name="hidden border-r border-gray-200 bg-gray-100/40 md:block",
    )


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(class_name="w-full flex-1"),
        rx.cond(
                AuthState.current_user_role,
                rx.el.button(
                        rx.icon("log-out", class_name="mr-2 h-4 w-4"),
                        "Logout",
                        on_click=AuthState.logout,
                        class_name="flex items-center text-sm font-medium text-gray-600 hover:text-red-600 transition-colors",
                ),
                   
                rx.box(
                    rx.el.a(
                        rx.icon("circle-dot", class_name="h-6 w-6 text-emerald-600"),
                        rx.el.span("RDTire-APP", class_name="font-semibold"),
                        href="/",
                        class_name="flex items-center gap-2 font-semibold",
                    ),
                    rx.button(
                        rx.icon("log-in", class_name="mr-2 h-4 w-4"),
                        "Login",
                        on_click=lambda: rx.redirect("/login"),
                        class_name="flex items-center text-sm font-medium text-gray-600 hover:text-emerald-600 transition-colors",
                    ),
                    class_name="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6",
                ),    
        ),
        rx.el.button(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={AuthState.current_user['username']}",
                class_name="h-8 w-8 rounded-full",
            ),
            class_name="rounded-full border-2 border-transparent hover:border-emerald-600",
        ),
        class_name="flex h-14 items-center gap-4 border-b border-gray-200 bg-gray-100/40 px-4 lg:h-[60px] lg:px-6",
    )


def main_layout(child: rx.Component, *args, **kwargs) -> rx.Component:
    
    return rx.box(
        sidebar(),
        rx.box(
            header(),
            rx.el.main(
                child, class_name="flex flex-1 flex-col gap-4 p-4 md:gap-8 md:p-6"
            ),
            class_name="flex flex-col flex-1 overflow-auto",
        ),
        class_name="grid min-h-screen w-full md:grid-cols-[220px_1fr] lg:grid-cols-[220px_1fr]",
    )

