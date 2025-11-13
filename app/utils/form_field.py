import reflex as rx
from typing import List


def form_field_despegable(titulo: str, sel_campo: List, nombre: str, on_change: callable) -> rx.Component:
    return rx.flex(
        rx.badge(titulo, variant="solid", high_contrast=True),                
        rx.select(
            sel_campo,
            name=nombre,
            required=True,
            on_change=on_change,
        ),
        spaceing="2",
        width="100%",
        flex_direction=["column", "row", "column"],
    )


def form_field_input(titulo: str, placehol: str, nombre: str, tipo: str, max: int) -> rx.Component:
    return rx.flex(
        rx.badge(titulo, variant="solid", high_contrast=True),
        rx.input(
            placeholder=placehol,
            name=nombre,
            type= tipo,
            max_length = max,
            required=True,
        #on_blur="",
        ),
        width="100%",
        flex_direction=["column", "row", "column"],
    )


def form_field_onblur(label: str, name: str, type: str, on_blur) -> rx.Component:
    return rx.form.field(
            rx.form.label(label, class_name="font-medium text-sm"),
            rx.form.control(
                rx.input(
                    placeholder=f"Ingresa {label.lower()}",
                    name=name,
                    type=type,
                    on_blur=on_blur,
                    class_name="w-full p-2 border rounded-md mt-1",
                ),
                as_child=True,
                class_name="mb-4",
            ),
            name=name,
        )

def form_field_onchange(titulo: str, sel_campo: List, nombre: str, on_change: callable) -> rx.Component:
    return rx.flex(
        rx.badge(titulo, variant="solid", high_contrast=True),                
        rx.select(
            sel_campo,
            name=nombre,
            required=True,
            on_change=on_change,
        ),
        width="100%",
        flex_diretion=["column", "row", "column"],
    )


def form_field_change(label: str, name: str, value: str, placeholder: str, type: str) -> rx.Component:
        return rx.el.div(
            rx.el.label(label, class_name="text-sm font-medium text-emerald-600"),
            rx.el.input(
                placeholder=placeholder,
                name=name,
                type=type,
                default_value=value,
                class_name="w-full p-2 border border-gray-100 rounded-md mt-1",
            ),
        )

def form_field_password(label: str, name: str,  placeholder: str, type: str, read_only: bool) -> rx.Component:
        return rx.el.div(
            rx.el.label(label, class_name="text-sm font-medium text-emerald-600"),
            rx.el.input(
                placeholder=placeholder,
                name=name,
                type=type,
                required=True,
                read_only=read_only,
                class_name="w-full p-2 border border-gray-100 rounded-md mt-1",
            ),
        )

def form_field_desable(label: str, name: str,  placeholder: str, type: str, value: callable) -> rx.Component:
        return rx.el.div(
            rx.el.label(label, class_name="text-sm font-medium text-emerald-600"),
            rx.el.input(
                placeholder=placeholder,
                name=name,
                type=type,
                value=value,
                required=True,
                read_only=True,
                class_name="w-full p-2 border border-gray-100 rounded-md mt-1",
            ),
        )