import reflex as rx
from app.utils.constant import (
    ADMIN_NAV,
    TECNICO_NAV,
    USER_ADMIN_NAV,
    INICIO_NAV,
    ESTILO_BOTON_PRINCIPAL,
)
from app.states.auth_state import AuthState


def sidebar_item(item: dict) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(item["icon"], size=20, color="#14e9c5f2"),
            rx.text(item["name"], size="3", color="#fbfdfdf1"),
            width="100%",
            #padding_x="0.5rem",
            #padding_y="0.5rem",
            align="center",
            style={
                "_hover": {
                    "bg": rx.color("cyan"),
                    "color": "#0b0c0cf1", 
                },
                "border-radius": "1.5em",
            },
        ),
        href=item["path"],
        underline="none",
        color_scheme="cyan",
        style={
                "_hover": {
                    "color": "#0b0c0cf1", 
                },
 
            },
        weight="medium",
        width="100%",
    )


def sidebar_items() -> rx.Component:
    return rx.vstack(
        rx.match(
                    AuthState.current_user_role,
                    ("Administrador", rx.foreach(ADMIN_NAV, sidebar_item)),
                    ("Usuario Administrador", rx.foreach(USER_ADMIN_NAV, sidebar_item)),
                    ("Usuario Técnico", rx.foreach(TECNICO_NAV, sidebar_item)),
                ),
        # sidebar_item("Dashboard", "layout-dashboard", "/#"),
        # sidebar_item("Projects", "square-library", "/#"),
        # sidebar_item("Analytics", "bar-chart-4", "/#"),
        # sidebar_item("Messages", "mail", "/#"),
        spacing="1",
        width="100%",
    )


def sidebar_redx() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.vstack(
                rx.hstack(
                    
                    rx.box(
                        rx.flex(
                            rx.icon("circle-dot", color="#14e9c5f2", size=20),
                            rx.text("RDTire-APP", size="5", weight="medium", color="#fbfcfcf1"),
                            
                            direction="row",
                            gap="3",
                            padding="2",
                            align="center",
                        ),
                        size="2",
                        radius="full",
                        color_scheme="gray",
                        href="/redxtire",
                    ),
   
                    align="center",
                    justify="start",
                    padding_x="0.5rem",
                    width="100%",
                ),
                rx.divider(),
                sidebar_items(),
                rx.spacer(),
                rx.vstack(
                    rx.vstack(
                        rx.text(AuthState.cliente_actual['nombre'], size="5", weight="medium", color="#fbfdfdf1"),
                        rx.el.button(
                            rx.icon("log-out", color="#14e9c5f2"),
                            "Salir ",
                            on_click=AuthState.logout,
                            class_name="flex items-center text-lm font-medium text-gray-400 hover:text-red-400 transition-colors",
                        ),
                        
                        spacing="1",
                        width="100%",
                    ),
                    rx.divider(),
                    rx.hstack(
                        rx.icon_button(rx.icon("user", size=20)),
                        rx.vstack(
                            rx.box(
                                rx.text(AuthState.current_user["username"], size="3", weight="bold", color="#fbfdfdf1"),
                                rx.text(AuthState.current_user["email"], size="2", weight="medium", color="#08f1f1e8"),
                                width="100%",
                            ),
                            spacing="0",
                            align="start",
                            justify="start",
                            width="100%",
                        ),
                        padding_x="0.5rem",
                        align="center",
                        justify="start",
                        width="100%",
                    ),
                    width="100%",
                    spacing="5",
                ),
                spacing="3",
                # position="fixed",
                # left="0px",
                # top="0px",
                #z_index="100",
                padding_x="1em",
                padding_y="1.5em",
                bg="#063852",
                align="start",
                # height="100%",
                height="650px",
                width="14em",
            ),
        ),
        rx.mobile_and_tablet(
            rx.drawer.root(
                rx.drawer.trigger(rx.icon("align-justify", size=30)),
                rx.drawer.overlay(z_index="5"),
                rx.drawer.portal(
                    rx.drawer.content(
                        rx.vstack(
                            rx.box(
                                rx.drawer.close(rx.icon("x", size=30)),
                                width="100%",
                            ),
                            sidebar_items(),
                            rx.spacer(),
                            rx.vstack(
                                rx.vstack(
                                    rx.el.button(
                                        rx.icon("log-out", class_name="mr-2 h-4 w-4"),
                                        "Logout",
                                        on_click=AuthState.logout,
                                        class_name="flex items-center text-sm font-medium text-gray-600 hover:text-red-600 transition-colors",
                                    ),
                                    
                                    width="100%",
                                    spacing="1",
                                ),
                                rx.divider(margin="0"),
                                rx.hstack(
                                    rx.vstack(
                                        #rx.icon("user", size="3", color="gray.700")
                                        rx.box(
                                            
                                            rx.text(
                                                AuthState.current_user["username"], size="3", weight="bold"
                                            ),
                                            rx.text(
                                                AuthState.current_user["email"],
                                                size="2",
                                                weight="medium",
                                            ),
                                            width="100%",
                                        ),
                                        spacing="0",
                                        justify="start",
                                        width="100%",
                                    ),
                                    padding_x="0.5rem",
                                    align="center",
                                    justify="start",
                                    width="100%",
                                ),
                                width="100%",
                                spacing="5",
                            ),
                            spacing="5",
                            width="100%",
                        ),
                        top="auto",
                        right="auto",
                        height="100%",
                        width="20em",
                        padding="1.5em",
                        bg="#ffffffd5",
                    ),
                    width="100%",
                ),
                direction="left",
            ),
            padding="1em",
        ),
    )