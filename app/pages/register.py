import reflex as rx
from app.utils.constant import NOMBRE_APLICACION
from app.states.auth_state import AuthState

def register_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                rx.icon("circle-dot", class_name="h-8 w-8 text-emerald-600"),
                rx.el.span(NOMBRE_APLICACION, class_name="text-2xl font-bold"),
                href="/",
                class_name="flex items-center gap-2 font-semibold mb-8",
            ),
            rx.el.h1("Registro", class_name="text-3xl font-bold mb-2"),
            rx.el.p(
                "Crea una nueva cuenta para acceder al sistema.",
                class_name="text-gray-500 mb-6",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label("Nombre de usuario", class_name="font-medium text-sm"),
                    rx.el.input(
                        placeholder="Elige un nombre de usuario",
                        name="username",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Correo electrónico", class_name="font-medium text-sm"),
                    rx.el.input(
                        placeholder="Ingresa tu correo",
                        name="email",
                        type="email",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label("Contraseña", class_name="font-medium text-sm"),
                    rx.el.input(
                        placeholder="Crea una contraseña",
                        name="password",
                        type="password",
                        class_name="w-full p-2 border rounded-md mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.button(
                    "Registrarse",
                    type="submit",
                    class_name="w-full bg-emerald-600 text-white p-3 rounded-lg font-bold hover:bg-emerald-700 transition-colors",
                ),
                rx.el.div(
                    "¿Ya tienes una cuenta? ",
                    rx.el.a(
                        "Inicia sesión aquí",
                        href="/login",
                        class_name="text-emerald-600 hover:text-emerald-700 font-semibold",
                    ),
                    class_name="text-center mt-4 text-sm text-gray-600",
                ),
                on_submit=AuthState.register,
            ),
            class_name="w-full max-w-md bg-white p-8 rounded-2xl shadow-lg border",
        ),
        class_name="w-screen h-screen flex items-center justify-center bg-gray-50 font-['Raleway']",
    )