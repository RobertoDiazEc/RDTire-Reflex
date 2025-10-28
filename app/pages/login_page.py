import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("circle-dot", class_name="h-8 w-8 text-emerald-600"),
                rx.el.span("RDTire-Trading", class_name="text-2xl font-bold"),
                href="/",
                class_name="flex items-center gap-2 font-semibold mb-8",
            ),
            rx.el.h1("Login", class_name="text-3xl font-bold mb-2"),
            rx.el.p(
                "Enter your credentials to access your account.",
                class_name="text-gray-500 mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Username", class_name="font-medium text-sm"),
                    rx.el.input(
                        placeholder="Enter your username",
                        name="username",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Password", class_name="font-medium text-sm"),
                    rx.el.input(
                        placeholder="Enter your password",
                        name="password",
                        type="password",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.cond(
                    AuthState.error_message != "",
                    rx.el.div(
                        rx.icon("flag_triangle_right", class_name="h-4 w-4 mr-2"),
                        AuthState.error_message,
                        class_name="flex items-center bg-red-100 text-red-700 p-3 rounded-md mb-6 text-sm",
                    ),
                ),
                rx.el.button(
                    "Sign In",
                    type="submit",
                    class_name="w-full bg-emerald-600 text-white p-3 rounded-lg font-bold hover:bg-emerald-700 transition-colors",
                ),
                on_submit=AuthState.login,
            ),
            class_name="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg border",
        ),
        class_name="w-screen h-screen flex items-center justify-center bg-gray-50 font-['Raleway']",
    )