import reflex as rx
from app.utils.constant import NOMBRE_APLICACION, ROUTE_HOME
from app.states.cliente_state import ClienteState
from app.utils.campos import form_field_onblur



def datosCliente():
    return rx.form.root(
        form_field_onblur(
            "Nombre Completo",
            "nombre",
            "text",
            ClienteState.nombre_cliente,
        ),
        form_field_onblur(
            "Ciudad",
            "ciudad",
            "text",
            ClienteState.ciudad_cliente,
        ),
        form_field_onblur(
            "Contacto",
            "contacto",
            "text",
            ClienteState.contacto_cliente,
        ),
        
        rx.button(
            "Continuar",
            type="submit",
            class_name="w-full bg-emerald-600 text-white p-3 rounded-lg font-bold hover:bg-emerald-700 transition-colors",
        ),
        class_name="w-full",
        on_submit=ClienteState.register_client,
        reset_on_submit=True,

 )  

def register_page() -> rx.Component:
    return rx.box(
        datosCliente(),
        class_name="max-w-md mx-auto mt-20 p-8 bg-white rounded-lg shadow-md",
    )