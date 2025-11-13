import reflex as rx
import re
import bcrypt
from app.states.base_state import BaseState
from app.states.auth_state import AuthState
from app.database.db_rdtire import Usuario, Cliente
from app.database.schemas import UsuarioSchemaNuevo, UsuarioSchemaEditar
from typing import List
from pydantic import ValidationError


class UsersState(BaseState):
    form_data: dict = {}
    errors: dict = {}
    has_error: bool = False
    show_usuario_modal: bool = False
    is_editing_usuario: bool = False
    is_editing_usuario_password: bool = False
    selected_usuario: Usuario | None = None
    new_usuario: Usuario = Usuario()
    mostrar_usuario_tabla: bool = False
    code_password_usuario: str = ""
    edito_hash = False

    # @rx.event
    # def on_load(self):
    #     self.show_usuario_modal = False
    #     self.is_editing_usuario = False
    #     self.selected_usuario = None
    #     self.new_usuario = Usuario()
    #     self.clientes_actual = AuthState.cliente_actual()
    #     print("CUENTA: ")
    #     with rx.session() as session:
    #        self.usuario = session.exec(
    #             Usuario.select().where(Usuario.cliente_id == self.clientes_actual.id) 
    #         ).all()
    #        print("Usuarios cargados: ")


    @rx.event
    def open_add_usuario_modal(self):
        self.is_editing_usuario = False
        self.new_usuario = Usuario()
        self.show_usuario_modal = True
        

    @rx.event
    def mostrar_usuarios(self, cliente_id: int):
        self.mostrar_usuario_tabla = True
        with rx.session() as session:
            self.usuarios= session.exec(
                               Usuario.select().where(
                                    Cliente.id == cliente_id
                                )
                            ).all()
        

    @rx.event
    def open_edit_usuario_modal(self, usuario: Usuario):
        self.is_editing_usuario = True
        self.new_usuario = usuario
        self.selected_usuario = usuario
        self.show_usuario_modal = True
        
        
    @rx.event
    def open_edit_password_usuario_modal(self, usuario: Usuario):
        self.is_editing_usuario_password = True
        self.new_usuario = usuario
        self.selected_usuario = usuario
        self.show_usuario_modal = True


    @rx.event
    def close_usuario_modal(self):
        self.show_usuario_modal = False
        self.selected_usuario = None
        self.is_editing_usuario = False
        self.is_editing_usuario_password = False
        self.code_password_usuario = ""
        self.edito_hash = False

    @rx.event
    def handle_usuario_change(self, field: str, value: str):
        self.new_usuario[field] = value

    @rx.event
    def reset_form(self):
         self.form_data = {}
         self.errors = {}

    @rx.event
    def editando_hash(self, edito_hash):
        self.edito_hash = edito_hash

    @rx.event
    def save_usuario(self, form_data: dict):
        self.form_data = form_data
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, self.form_data["email"]):
            return rx.window_alert("Correo no válido")
        

        #print(code_password.decode())
        with rx.session() as session:
            if self.is_editing_usuario and self.selected_usuario:
                if session.exec(
                    Usuario.select()
                    .where(Usuario.email == self.form_data["email"])
                    .where(Usuario.id != self.new_usuario.id)
                    ).first():
                    return rx.window_alert("Email ya existe ... No puede cambiar")
                if session.exec(
                    Usuario.select()
                    .where(Usuario.username == self.form_data["username"])
                    .where(Usuario.id != self.new_usuario.id)
                    ).first():
                    return rx.window_alert("Username ya existe ... No puede cambiar")
                
                try:
                    #print(self.form_data)
                    instance_data = UsuarioSchemaEditar.model_validate(form_data)
                except ValidationError as e:
                    for err in e.errors():
                        field_name = err['loc'][0] if err['loc'] else 'general'
                        self.errors[field_name] = err['msg']
                    self.has_error = True 
                    return  rx.window_alert(self.errors)  
                except Exception as er:
                    self.has_error = True
                    self.errors = {
                        "general": f"se genero un error : {str(er)}"
                    }
                    return rx.window_alert(self.errors())
                usuario_actual=session.exec(
                    Usuario.select()
                    .where(Usuario.id == self.new_usuario.id)
                    ).first()
                usuario_actual.username = instance_data.username
                usuario_actual.email = instance_data.email
                usuario_actual.role = instance_data.role
                
                #print(instance)
                session.add(usuario_actual)

                session.commit()

                #session.refresh(instance)
            else:
                if self.form_data["password_hash"] != self.form_data["confirma_password_hash"]:
                    return rx.window_alert("Passwords no es igual.")
                
                code_password =  bcrypt.hashpw(self.form_data["password_hash"].encode(), bcrypt.gensalt())
                self.form_data["password_hash"] = code_password.decode()
                form_data["password_hash"] = code_password.decode()
                if session.exec(Usuario.select().where(Usuario.email == self.form_data["email"])).first():
                    return rx.window_alert("Email ya existe.")
                if session.exec(Usuario.select().where(Usuario.username == self.form_data["username"])).first():
                    return rx.window_alert("Username ya existe")
                
                try:
                    #print(self.form_data)
                    instance_data = UsuarioSchemaNuevo.model_validate(form_data)
                except ValidationError as e:
                    for err in e.errors():
                        field_name = err['loc'][0] if err['loc'] else 'general'
                        self.errors[field_name] = err['msg']
                    self.has_error = True 
                    return  rx.window_alert(self.errors)  
                except Exception as er:
                    self.has_error = True
                    self.errors = {
                        "general": f"se genero un error : {str(er)}"
                    }
                    return rx.window_alert(self.errors())
                
                instance = Usuario(**instance_data.model_dump())
                #print(instance)
                session.add(instance)

                session.commit()

                session.refresh(instance)
        self.close_usuario_modal()