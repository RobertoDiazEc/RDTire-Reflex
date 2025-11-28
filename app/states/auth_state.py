import reflex as rx
import re
import bcrypt
from typing import TypedDict, Literal
import hashlib
import logging
from app.states.base_state import BaseState
from app.database.db_rdtire import Usuario, Cliente
from decouple import config

USER_MAESTRO_REDX = config("USER_MAESTRO_REDX")
PASSWORD_MAESTRO_REDX = config("PASSWORD_MAESTRO_REDX")

# BASE_API_URL = "tu_url_api_aqui"
Role = Literal["Administrador", "Usuario Administrador", "Usuario Técnico"]





class AuthState(BaseState):
    error_message: str = ""
    is_authenticated: bool = False
    #current_user: User | None = None
    current_user: Usuario = Usuario()
    cliente_actual: Cliente = Cliente()
    user_role: str = ""
    intent_login: bool = False
    numero_intentos: int = 0
    cliente_id_actual: int = 0

    @rx.event
    def login(self, form_data: dict):
        self.error_message = ""
        username = form_data.get("username", "").strip().lower()
        password = form_data.get("password", "").strip()
  
        if not username or not password:
            self.error_message = "Username y password son requeridos."
            return
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, username):
            return rx.window_alert("Correo no válido")
        #print( username + " -- " + password)
        self.numero_intentos = self.numero_intentos + 1
        try:
            if self.numero_intentos > 4:
                self.error_message = "Cierre la pagina y vuelva a intentarlo. Número máximo de intentos de login excedido."
                self.intent_login = True
                return rx.window_alert("Número máximo de intentos de login excedido.")
            
            with rx.session() as session:
                obj = session.exec(
                        Usuario.select().where(
                            Usuario.email == username
                        )
                    ).first()
                
                if obj:
                    code_password = obj.password_hash
                    if bcrypt.checkpw(password.encode(), code_password.encode()):
                        self.is_authenticated = True
                        self.current_user = obj
                        self.user_role = obj.role
                        self.cliente_id_actual = obj.cliente_id
                        self.cliente_actual= session.exec(
                               Cliente.select().where(
                                    Cliente.id == obj.cliente_id
                                )
                            ).first()
                        return rx.redirect("/redxtire")
                
                    # password_hash = hashlib.sha256(password.encode()).hexdigest()
                    # if password_hash != db_user.password_hash:
                else:
                    
                    if username == USER_MAESTRO_REDX and password == PASSWORD_MAESTRO_REDX:
                        
                        self.is_authenticated = True
                        self.user_role = "Administrador"
                        self.current_user = {
                            "username": USER_MAESTRO_REDX,
                            "password_hash": PASSWORD_MAESTRO_REDX,
                            "role": "Administrador",
                            "client_id": 0,
                            "schema_name": "public",                           
                        }
                           
                        return rx.redirect("/redxtire")
                    self.error_message = "Inválido el password o username."
                    return rx.window_alert("Inválido el password o username.")
        
        except Exception as e:       
            return rx.window_alert(f"Error Ingreso Login-Usuario {form_data.get("username")}, error:--> {e}")

    @rx.event
    def logout(self):
        self.is_authenticated = False
        self.current_user = None
        self.error_message = ""
        self.intent_login = False
        self.numero_intentos = 0
        return rx.redirect("/")

    @rx.var
    def current_user_role(self) -> str:
        if self.current_user:
            return self.current_user.role
        return ""

    @rx.var
    def client_schema(self) -> str:
        if self.current_user:
            return "public"
        return "public"

    @rx.event
    def require_login(self) -> rx.event.EventSpec | None:
        if not self.is_authenticated:
            return rx.redirect("/login")
        return self.inicializar_datos()
    
    @rx.event
    def inicializar_datos(self):
        self.cliente_id_global = self.cliente_id_actual

    @rx.event
    def require_role(self, required_roles: list[Role]) -> rx.event.EventSpec | None:
        if not self.is_authenticated:
            return rx.redirect("/login")
        if self.current_user and self.current_user.role not in required_roles:
            logging.warning(
                f"User {self.current_user.username} with role {self.current_user.role} tried to access a page requiring one of {required_roles}"
            )
            return rx.redirect("/")
        return None
    
    @rx.event
    def hash_password(password: str) -> str:
        """Genera un hash seguro de la contraseña usando bcrypt."""
        
        # 1. Generar un 'salt' (valor aleatorio) único para esta contraseña.
        # El salt ayuda a proteger contra ataques de tablas arcoíris.
        salt = bcrypt.gensalt()
        
        # 2. Generar el hash combinando la contraseña con el salt.
        # Necesitas codificar la contraseña a bytes antes de hashear.
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # 3. Decodificar a str para guardar en la base de datos (PostgreSQL/SQLModel)
        return hashed.decode('utf-8')