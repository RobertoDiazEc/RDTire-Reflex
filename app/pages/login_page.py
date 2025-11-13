import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.card(
        rx.el.div(
            rx.el.a(
                rx.icon("circle-dot", class_name="h-8 w-8 text-emerald-600"),
                rx.el.span("RDTire-App", class_name="text-2xl font-bold"),
                href="/",
                class_name="flex items-center gap-2 font-semibold mb-8",
            ),
            rx.el.h1("Ingrese", class_name="text-3xl font-bold mb-2"),
            rx.el.p(
                " sus credenciales para acceder a su cuenta.",
                class_name="text-gray-500 mb-6",
            ),
            rx.form(
                rx.el.div(
                    rx.el.label("Email Usuario", class_name="font-medium text-sm"),
                    rx.el.input(
                        placeholder="Ingrese su email",
                        name="username",
                        class_name="w-full p-2 border border-gray-200 rounded-md mt-1",
                        type="email",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Password", class_name="font-medium text-sm"),
                    rx.el.input(
                        placeholder="Ingrese su password",
                        name="password",
                        type="password",
                        class_name="w-full p-2 border border-gray-200 rounded-md mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.box(
                        rx.icon("flag_triangle_right", class_name="h-4 w-4 mr-2"),
                        AuthState.error_message,
                        class_name="flex items-center bg-red-100 text-red-700 p-3 rounded-md mb-6 text-sm",
                    ),
                ),
                rx.button(
                    "Iniciar Sesión",
                    type="submit",
                    disabled=AuthState.intent_login,
                    class_name="w-full bg-emerald-600 text-white p-3 rounded-lg font-bold hover:bg-emerald-700 transition-colors",
                ),
                rx.box(
                    "¿No tienes una cuenta? ",
                    rx.el.a(
                        "Regístrate aquí",
                        href="/register",
                        class_name="text-emerald-600 hover:text-emerald-700 font-semibold",
                    ),
                    class_name="text-center mt-4 text-sm text-gray-600",
                ),
                on_submit=AuthState.login,
            ),
            class_name="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg border border-gray-200",
        ),
        class_name="w-screen h-screen flex items-center justify-center bg-gray-50 font-['Raleway'] ",
    )