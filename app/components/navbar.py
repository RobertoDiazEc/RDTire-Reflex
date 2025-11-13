import reflex as rx
from app.utils.constant import ESTILO_BOTON_PRINCIPAL

def mobile_navbar_link(url:str):
    return rx.redirect(url)

def navbar_buttons() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.el.a(
                            rx.icon(
                                "circle-dot", class_name="h-6 w-6 text-emerald-600"
                            ),
                            rx.el.span(
                                "RDTire-APP",
                                class_name="text-3xl md:text-3xl font-bold font-semibold ",
                            ),
                            href="/",
                            class_name="flex items-center gap-2 font-semibold",
                        ),
                        class_name="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6",
                    )
                ),
                rx.hstack(
                    rx.button(
                        rx.icon("user-lock", class_name="mr-2 h-4 w-4 size='lg'"),
                        "Login",
                        on_click=lambda: rx.redirect("/login"),
                        class_name=ESTILO_BOTON_PRINCIPAL,
                    ),
                    rx.button(
                        rx.icon("user-round-plus", class_name="mr-2 h-4 w-4 size='lg'"),
                        "Registrate",
                        on_click=lambda: rx.redirect("/register"),
                        class_name=ESTILO_BOTON_PRINCIPAL,
                        transition_colors=True,
                    ),
                    spacing="4",
                    justify="end",
                ),
                justify="between",
                align_items="center",
            )
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.box(
                        rx.icon("circle-dot", class_name="h-6 w-6 text-emerald-600"),
                        rx.el.span("RDTire-APP", class_name="font-semibold"),
                        class_name="flex items-center gap-2 font-semibold",
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        rx.menu.item("Log in", on_click=lambda: mobile_navbar_link("/login")),
                        rx.menu.item("Sign up", on_click=lambda: mobile_navbar_link("/register")),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            )
        ),
        clase_name="bg-white shadow-sm w- w-full overflow-hidden",
        width="100%",
    )