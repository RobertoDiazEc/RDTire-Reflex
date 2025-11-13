import reflex as rx
from app.states.users_state import UsersState
from app.states.auth_state import AuthState
from app.database.db_rdtire import Usuario
from app.utils.form_field import form_field_change,form_field_password,form_field_desable
from app.utils.campos import boton_icon
from app.utils.routes import Route
from app.components.layout import main_layout


def usuario_list_item(usuarios: Usuario) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={usuarios.username}",
                    class_name="h-10 w-10 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(usuarios.username, class_name="font-medium"),
                    
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="p-3",
        ),
        rx.el.td(rx.el.p(usuarios.email, class_name="text-sm text-gray-500"),),
        rx.el.td(usuarios.role, class_name="p-3"),
        rx.el.td(usuarios.activo, class_name="p-3"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "Editar",
                    on_click=lambda: UsersState.open_edit_usuario_modal(usuarios),
                    class_name="text-blue-600 hover:underline ml-4",
                ),
                rx.el.button(
                    "Cambiar Password",
                    on_click=lambda: UsersState.open_edit_password_usuario_modal(usuarios), 
                    class_name="text-emerald-600 hover:underline"
                ),
            ),
            class_name="p-3 text-right",
        ),
    )

def input_password_usuario() -> rx.Component:
    return  rx.el.div(                    
            form_field_password(
                "Password",
                "password_hash",
                "*********************",                            
                "password",
                False
            ),
            form_field_password(
                "Confirmar Password",
                "confirma_password_hash",
                "**********************",
                "password",
                False
            ), 
    )

def usuario_modal() -> rx.Component:
    return rx.cond(
        UsersState.show_usuario_modal,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            UsersState.is_editing_usuario,
                            "Editar ",
                            "Nuevo",
                        ),
                        class_name="text-xl font-bold",
                    ),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=UsersState.close_usuario_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-center pb-4 border-b bg-white",
                    
                ),
                rx.el.form(
                    rx.el.div(
                        form_field_change(
                            "Nombre",
                            "username",
                            UsersState.new_usuario['username'],
                            "e.g. John Doe",
                            "text",
                        ),
                        form_field_change(
                            "Email",
                            "email",
                            UsersState.new_usuario['email'],
                            "e.g. john@example.com",
                            "email",
                        ),
                        form_field_change(
                            "Rol",
                            "role",
                            UsersState.new_usuario['role'],
                            "Usuario Técnico",
                            "text",
                        ), 
                         rx.cond(
                            UsersState.is_editing_usuario,
                            None,
                            rx.el.div(
                                form_field_password(
                                    "Password",
                                    "password_hash",
                                    "*********************",                            
                                    "password",
                                    False
                                ),
                                form_field_password(
                                    "Confirmar Password",
                                    "confirma_password_hash",
                                    "**********************",
                                    "password",
                                    False
                                ),
                            ), 
                         ),   
                        form_field_desable(
                            "Cliente",
                            "cliente_id",
                            "cliente solo lectura",
                            "text",
                            AuthState.current_user["cliente_id"],
                        ),
                        class_name="grid grid-cols-1 gap-4 py-4",
                    ),
                          
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=UsersState.close_usuario_modal,
                            class_name="px-4 py-2 bg-gray-200 rounded-md",
                            type="button",
                        ),
                        rx.el.button(
                            "Guardar Cambios",
                            type="submit",
                            class_name="px-4 py-2 bg-emerald-600 text-white rounded-md",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t",
                    ),
                    on_submit=UsersState.save_usuario,
                    class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-4xl",
                )
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50", 
        ),
    )

def usuario_edit_lateral(usuarios: Usuario) -> rx.Component:
    return rx.el.div(
        rx.button("Editar", on_click=UsersState.open_edit_usuario_modal(usuarios)),
        rx.cond(
            UsersState.is_editing_usuario,
            usuario_modal(), 
        ),
        class_name="p-1 md:p-1"

    )


def usuario_new_edit() -> rx.Component:
 
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                rx.icon("plus", size=20),
                rx.text("Nuevo ", size="3"),
                on_click=UsersState.open_add_usuario_modal,
                ),
        ),
        rx.dialog.content(
            rx.dialog.title(
            "Nuevo Usuario",
            ),
            #  rx.dialog.description(
            #      "Rellene el formulario con la información del usuario",
            #  ),
            # usuario_modal(),
            rx.form(
                rx.flex(
                   form_field_change(
                            "Nombre",
                            "username",
                            "",
                            "e.g. John Doe",
                            "text",
                        ),
                        form_field_change(
                            "Email",
                            "email",
                            "",
                            "e.g. john@example.com",
                            "email",
                        ),
                        form_field_change(
                            "Rol",
                            "role",
                            "",
                            "Usuario Técnico",
                            "text",
                        ), 
                         rx.cond(
                            UsersState.is_editing_usuario,
                            None,
                            rx.el.div(
                                form_field_password(
                                    "Password",
                                    "password_hash",
                                    "*********************",                            
                                    "password",
                                    False
                                ),
                                form_field_password(
                                    "Confirmar Password",
                                    "confirma_password_hash",
                                    "**********************",
                                    "password",
                                    False
                                ),
                            ), 
                         ),   
                        form_field_desable(
                            "Cliente",
                            "cliente_id",
                            "cliente solo lectura",
                            "text",
                            AuthState.current_user["cliente_id"],
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
                            rx.button("Grabar", type="submit"),
                        ),
                        spacing="3",
                        justify="end",
                    ),
                    direction="column",
                    spacing="4",
                ),
                on_submit=UsersState.save_usuario,
                reset_on_submit=False,
            ),
           max_width="450px",
         )
    )

def show_usuarios(usuarios: Usuario):
    """Show a usuarios in a table row."""
    return rx.table.row(
        rx.table.cell(
            rx.hstack(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={usuarios.username}",
                    class_name="h-10 w-10 rounded-full",
                ),
                usuarios["username"],
                padding_x="0.5rem",
                flex_wrap="wrap",
                align_items="center",
                ),),
        rx.table.cell(usuarios["email"]),
        rx.table.cell(usuarios["role"]),
        rx.table.cell(usuarios["activo"]),
        rx.table.cell(usuario_edit_lateral(usuarios))
    )

@rx.page(route=Route.USERS.value,
         on_load=lambda: AuthState.require_role(["Administrador", "Usuario Administrador"]),
         )
def users_page() -> rx.Component:
    return main_layout(
        rx.el.div(
        rx.el.div(
            # rx.el.h1(f{"usuarios para " {}}, class_name="text-3xl font-bold"),
            rx.el.p("Administración de Usuarios.", class_name="text-gray-500"),
            # rx.el.button(
            #     "Nuevo Usuario",
            #     on_click=UsersState.open_add_usuario_modal,
            #     class_name="px-4 py-2 bg-emerald-600 text-white rounded-md mt-4",
            # ),
            usuario_new_edit(),
         
            rx.button(
                rx.icon("table-cells-split", size=20),
                rx.text("Mostrar", size="3"),
                on_click=UsersState.mostrar_usuarios(AuthState.current_user["cliente_id"]),
            ),
            class_name="flex justify-center gap-2 pt-4 border-t",
        ),
      
        rx.vstack(
                
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.column_header_cell("Usuario"),
                            rx.table.column_header_cell("Email"),
                            rx.table.column_header_cell("Categoria"),
                            rx.table.column_header_cell("Estado"),
                            rx.table.column_header_cell(" ")
                        ),
                    ),
                    #rx.table.body(rx.foreach(DatabaseTableState.filtered_users, show_customer)),
                    rx.table.body((rx.foreach(UsersState.usuarios, show_usuarios)),
                    #on_mount=DatabaseTableState.load_entries,
                    width="100%",
                ),
                width="100%",
            ),
        ),
    ),
    )