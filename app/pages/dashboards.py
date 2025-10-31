import reflex as rx
from app.states.auth_state import AuthState
from app.components.layout import main_layout


def admin_dashboard() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.h1("Admin Dashboard", class_name="text-3xl font-bold"),
            rx.el.p(
                f"Bienvenido, {AuthState.current_user['username']}! You have full system access.",
                class_name="text-gray-600 center font-semibold",
            ),
        )
    )


def user_admin_dashboard() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.h1("User Admin Dashboard", class_name="text-3xl font-bold"),
            rx.el.p(
                f"Welcome, {AuthState.current_user['username']}! You can manage vehicles and tires.",
                class_name="text-gray-600",
            ),
        ),
    )


def tecnico_dashboard() -> rx.Component:
    return main_layout(
        rx.el.div(
            rx.el.h1("Technician Dashboard", class_name="text-3xl font-bold"),
            rx.el.p(
                f"Welcome, {AuthState.current_user['username']}! You can perform tire inspections.",
                class_name="text-gray-600",
            ),
        )
    )


