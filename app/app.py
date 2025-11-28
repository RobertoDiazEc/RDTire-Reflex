import reflex as rx

from app.states.base_state import BaseState
from app.states.auth_state import AuthState
from app.components.inicio_pag import inicio_section
from app.components.navbar import navbar_buttons
from app.components.footer import footer
from app.components.users import users_page

from app.pages.login_page import login_page
from app.pages.db_utils import IniciacionTire_page
from app.pages.redxtire import redxtire_page
import app.utils.constant as Constants
from app.utils.routes import Route

#RDTIRE_LOGO, ROUTE_HOME, ROUTE_LOGIN, ROUTE_REGISTER

def index() -> rx.Component:
    return rx.fragment(
        navbar_buttons(), 
        inicio_section(), 
        footer()
        )


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

title = "RDTire App"
description = "Maneja tus llantas eficientemente con RDTire App."
preview = Constants.RDTIRE_LOGO

app.add_page(index,
             route=Route.INDEX.value,
             title=title,
             description=description,
             image=preview,
             )
#app.add_page(index)

@rx.page(
    route=Route.PRODUCTS.value,
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def products_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.products import products_page_ui

    return main_layout(products_page_ui())


@rx.page(
    route=Route.INVENTORY.value,
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def inventory_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.inventory import inventory_page_ui

    return main_layout(inventory_page_ui())


@rx.page(
    route=Route.SALES.value,
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def sales_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.sales import sales_page_ui

    return main_layout(sales_page_ui())


@rx.page(
    route=Route.CUSTOMERS.value,
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def customers_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.customers import customers_page_ui

    return main_layout(customers_page_ui())


@rx.page(route=Route.REPORTS.value, on_load=lambda: AuthState.require_role(["Administrador"]))
def reports_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.reports import reports_page_ui

    return main_layout(reports_page_ui())


@rx.page(route=Route.ANALYTICS.value, on_load=lambda: AuthState.require_role(["Administrador"]))
def analytics_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.analytics import analytics_dashboard

    return main_layout(analytics_dashboard())


@rx.page(
    route=Route.INSPECTIONS.value,
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Técnico"]),
)
def inspections_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.inspections import inspections_ui

    return main_layout(inspections_ui())


@rx.page(
    route=Route.INSPECTIONSVEHICLE.value,
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Técnico"]),
)
def inspections_vehicle_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.inspecvehicle import inspeccion_vehiculo_ui

    return main_layout(inspeccion_vehiculo_ui())    


@rx.page(
    route=Route.VEHICLES.value,
    on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
)
def vehicles_page() -> rx.Component:
    from app.components.layout import main_layout
    from app.components.vehicles import vehicles_page_ui

    return main_layout(vehicles_page_ui()) 

app.add_page(login_page, route=Route.LOGIN.value)
app.add_page(redxtire_page, route=Route.APPTIRE.value)
app.add_page(products_page)
app.add_page(inventory_page)
app.add_page(sales_page)
app.add_page(customers_page)
app.add_page(users_page)
app.add_page(reports_page)
app.add_page(analytics_page)
app.add_page(inspections_page)
app.add_page(vehicles_page)
app.add_page(IniciacionTire_page, route=Route.INICIACION_TIRE.value)
app.add_page(inspections_vehicle_page)