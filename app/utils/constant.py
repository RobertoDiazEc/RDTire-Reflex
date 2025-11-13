from app.utils.routes import Route

NOMBRE_APLICACION = "RDTire-APP"

ESTILO_BOTON_PRINCIPAL = (
    "flex bg-[#00edc6] px-8 py-4 items-center text-sm font-semibold rounded-md text-black shadow-lg hover:bg-white transition-all duration-300 transition-colors transform hover:scale-105 hover:shadow-xl",
)


RDTIRE_LOGO = "app/assets/images/rdtire_logo.png"

ADMIN_NAV = [
    {"name": "Dashboard", "path": Route.APPTIRE.value, "icon": "layout-dashboard"},
    {"name": "Productos", "path": Route.PRODUCTS.value, "icon": "package"},
    {"name": "Inventario", "path": Route.INVENTORY.value, "icon": "boxes"},
    {"name": "Ventas", "path": Route.SALES.value, "icon": "shopping-cart"},
    {"name": "Usuarios", "path": Route.USERS.value, "icon": "users"},
    {"name": "Vehiculo", "path": Route.VEHICLES.value, "icon": "car"},
    {"name": "Inspección", "path": Route.INSPECTIONS.value, "icon": "search"},
    {"name": "Analisis", "path": Route.ANALYTICS.value, "icon": "bar-chart-3"},
    {"name": "Reportes", "path": Route.REPORTS.value, "icon": "file-text"},
    {"name": "Ajustes", "path": Route.SETTINGS.value, "icon": "settings"},
]
USER_ADMIN_NAV = [
    {"name": "Dashboard", "path": Route.APPTIRE.value, "icon": "layout-dashboard"},
    {"name": "Usuario", "path": Route.CUSTOMERS.value, "icon": "users"},
    {"name": "Vehiculo", "path": Route.VEHICLES.value, "icon": "car"},
    {"name": "Inspección", "path": Route.INSPECTIONS.value, "icon": "search"},
    {"name": "Reportes", "path": Route.REPORTS.value, "icon": "file-text"},
]
TECNICO_NAV = [
    {"name": "Dashboard", "path": Route.APPTIRE.value, "icon": "layout-dashboard"},
    {"name": "Inspección", "path": Route.INSPECTIONS.value, "icon": "search"},
]
INICIO_NAV = [{"name": "Dashboard", "path": Route.APPTIRE.value, "icon": "layout-dashboard"}]

meses_anio: dict = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
    }

FACEBOOK_URL = "https://www.facebook.com/profile.php?id=61565067518519"
TWITTER_URL = "https://twitter.com/REDxSoluciones"
INSTAGRAM_URL = "https://www.instagram.com/redxsoluciones/"
LINKEDIN_URL = "https://www.linkedin.com/company/redx-soluciones/"