import reflex as rx

from sqlmodel import Session, select
from app.database.db_rdtire import Usuario, Cliente, Roles
from app.states.auth_state import AuthState

import datetime
import logging
from typing import cast
import bcrypt
from decouple import config

EMAIL_ADMIN_REDX = config("EMAIL_ADMIN_REDX")
SUPER_ADMIN_PASSWORD_HASH = config("SUPER_ADMIN_PASSWORD_HASH")
SUPER_ADMIN = config("SUPER_ADMIN")
SUPER_ADMIN_ROLE = config("SUPER_ADMIN_ROLE")
# (Asumiendo que tienes una función para hashear contraseñas, ej: hash_password)



class Inicio_Setup_State(rx.State):
    """Estado para la inicialización del sistema y creación del Super Administrador."""
    existe_cliente: bool = False
    show_setup_admin_modal:  bool = False
    nombre_flota: str = ""
    ciudad_flota: str = ""
    codigo_cliente: str = "" 
    tipo_plan: str = ""
    plan_value: str = "BASICO"

    @rx.event
    def open_setup_admin_modal(self):
        """Abre el modal de configuración inicial."""
        pass
    
    @rx.event
    def ver_existe_cliente(self):
        """Verifica si ya existe al menos un cliente/flota en la base de datos."""
        with rx.session() as session:
            existing_clients = session.exec(Cliente.select()).first()
            if existing_clients:
                self.existe_cliente = True
            else:
                self.existe_cliente = False
        return         
        
    @rx.event
    def create_super_admin(self, form_data: dict):
        """Crea el primer cliente/flota y el usuario Super Administrador."""
        self.nombre_flota = form_data.get("nombre_flota", "REDx Tire").strip()
        self.ciudad_flota = form_data.get("ciudad_flota", "Quito").strip()
        self.codigo_cliente = form_data.get("codigo_cliente", "FLTA001").strip()
        self.tipo_plan = form_data.get("tipo_plan", "BASICO").strip()
        # 1. Conexión a la base de datos (Obtener la sesión)
        with rx.session() as session: # 'engine' es tu conexión a la DB           
            # 2. VERIFICACIÓN CRÍTICA: ¿Ya existen clientes/flotas?
            existing_clients = session.exec(Cliente.select()).first()
            if existing_clients:
                print("Inicialización omitida")
                return
            try:
            # 3. CREAR LA PRIMERA FLOTA/COMPAÑÍA (CRÍTICO)
                new_client = Cliente(
                    nombre=self.nombre_flota,
                    ciudad=self.ciudad_flota,
                    activo=True,
                    estado="AC",
                    codigo_cliente=self.codigo_cliente,
                    numero_vehiculos=2,
                    tipo_plan=self.tipo_plan,
                    fecha_creacion= datetime.datetime.now(
                        datetime.timezone.utc
                    )
                )
                session.add(new_client)
                session.flush() # Forzar la inserción para obtener el ID de la Flota
                rx.window_alert("Ingresando Cliente")
                new_role = Roles(
                    nombre=SUPER_ADMIN_ROLE,
                    descripcion="Rol con todos los permisos de administrador",
                )
                session.add(new_role)
                rx.window_alert("Rol Inicial creado")
                # 4. CREAR EL SUPER ADMINISTRADOR
                password = SUPER_ADMIN_PASSWORD_HASH
                hashed_password= bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                super_admin_user = Usuario(
                    email=EMAIL_ADMIN_REDX,
                    username=SUPER_ADMIN,
                    password_hash=hashed_password,
                    activo=True,
                    estado="AC",
                    fecha_creacion= datetime.datetime.now(
                        datetime.timezone.utc
                    ),
                    # Le asignamos el ID de la primera Flota creada
                    cliente_id=new_client.id, 
                    role=SUPER_ADMIN_ROLE, 
                    # ...
                )
                session.add(super_admin_user)
                rx.window_alert("Creado Usuario")        
                # 5. COMMIT FINAL
                session.commit()
                print(f"✅ Inicialización Completada '{self.nombre_flota}'.")
            except Exception as e:       
                return rx.window_alert(f"Error Ingreso Login-Usuario {form_data.get("username")}, error:--> {e}")
            
        return rx.window_alert("Inicialización completada. Por favor, inicie sesión con el usuario administrador.")



@rx.page(route="/setup-admin", on_load=Inicio_Setup_State.ver_existe_cliente)
def IniciacionTire_page() -> rx.Component:
    return rx.container(
        rx.box(
            rx.cond(
                Inicio_Setup_State.existe_cliente,
                rx.heading("La configuración inicial ya ha sido completada.",
                        justify="center",
                        align_items="center",
                        height="50vh",
                        color="red",
                        size="7"
                        ),
                rx.heading("Bienvenido a la configuración inicial de REDx Tire. ",
                        justify="center",
                        align_items="center",
                        height="50vh",
                        color="blue",
                        size="7"
                        ),      
                ),
            rx.cond(
                Inicio_Setup_State.existe_cliente,
                None,
                rx.box(
                    rx.dialog.root(
                        rx.dialog.trigger(
                            rx.button(
                                rx.icon("plus", size=26),
                                rx.text("Información Inicial", size="4"),
                            ),
                        ),
                        rx.dialog.content(
                            rx.dialog.title(
                                "Inicialización del Sistema",
                            ),
                            rx.form(
                                rx.flex(
                                    rx.input(placeholder="Nombre Cliente Inicial", name="name"),
                                    rx.input(placeholder="Ciudad de Operacion Inical", name="email"),
                                    rx.input(placeholder="Codigo Cliente Inicial", name="codigo_cliente"),
                                    rx.select(
                                        ["BASICO", "ESTANDAR", "PREMIUM"],
                                        value=Inicio_Setup_State.plan_value,                                        
                                        placeholder="Tipo de Plan",
                                        name="tipo_plan",
                                    ),
                                    rx.flex(
                                        rx.dialog.close(
                                            rx.button(
                                                "Cancelar",
                                                variant="soft",
                                                color_scheme="gray",
                                            ),
                                        ),
                                        rx.dialog.close(
                                            rx.button("Enviar Info Inicial", type="submit"),
                                        ),
                                        spacing="3",
                                        justify="end",
                                    ),
                                    direction="column",
                                    spacing="4",
                                ),
                                on_submit=Inicio_Setup_State.create_super_admin,
                                reset_on_submit=False,
                            ),
                            max_width="450px",
                        ),
                    ),
                    justify_content="center",
                    align_items="center",
                    height="50vh",
                ),               
            ),
            justify_content="center",
            align_items="center",
            height="50vh",
        ),  
        padding="50px",
        bg_color="gray.100",
        justify_content="center"

    )       