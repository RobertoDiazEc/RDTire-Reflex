import reflex as rx
from app.states.auth_state import AuthState
from app.components.inicio_pag import inicio_section
from app.components.navbar import navbar_buttons
from app.components.footer import footer
from app.pages.login_page import login_page
from app.pages.register import register_page
from app.pages.redxtire import redxtire_page


#on_load=AuthState.require_login
@rx.page()
def index() -> rx.Component:
    return rx.fragment(
        navbar_buttons(),
        inicio_section(),
        footer(),
    )


@rx.page(
    route="/products",
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def products_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.products import products_page_ui

    return main_layout(products_page_ui())


@rx.page(
    route="/inventory",
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def inventory_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.inventory import inventory_page_ui

    return main_layout(inventory_page_ui())


@rx.page(
    route="/sales",
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def sales_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.sales import sales_page_ui

    return main_layout(sales_page_ui())


@rx.page(
    route="/customers",
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def customers_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.customers import customers_page_ui

    return main_layout(customers_page_ui())


@rx.page(route="/reports", on_load=lambda: AuthState.require_role(["Administrador"]))
def reports_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.reports import reports_page_ui

    return main_layout(reports_page_ui())


@rx.page(route="/analytics", on_load=lambda: AuthState.require_role(["Administrador"]))
def analytics_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.analytics import analytics_dashboard

    return main_layout(analytics_dashboard())


@rx.page(
    route="/inspections",
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Técnico"]),
)
def inspections_page() -> rx.Component:
    from app.components.layout import main_layout

    return main_layout(rx.el.h1("Inspections Page"))


@rx.page(
    route="/vehicles",
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def vehicles_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.vehicles import vehicles_page_ui

    return main_layout(vehicles_page_ui())


app = rx.App(
    theme=rx.theme(appearance="light"),
    stylesheets=["/animations.css"],
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Raleway:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index)
app.add_page(login_page, route="/login")
app.add_page(register_page, route="/register")
app.add_page(redxtire_page, route="/redxtire")
app.add_page(products_page)
app.add_page(inventory_page)
app.add_page(sales_page)
app.add_page(customers_page)
app.add_page(reports_page)
app.add_page(analytics_page)
app.add_page(inspections_page)
app.add_page(vehicles_page)