import reflex as rx
from app.states.cliente_state import ClienteState
from app.states.base_state import Customer
from app.utils.campos import form_field_onblur


def cliente_list_item(customer: Customer) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.image(
                    src=f"https://api.dicebear.com/9.x/initials/svg?seed={customer['name']}",
                    class_name="h-10 w-10 rounded-full",
                ),
                rx.el.div(
                    rx.el.p(customer["name"], class_name="font-medium"),
                    rx.el.p(customer["email"], class_name="text-sm text-gray-500"),
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="p-3",
        ),
        rx.el.td(customer["phone"], class_name="p-3"),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    "View Profile", class_name="text-emerald-600 hover:underline"
                ),
                rx.el.button(
                    "Edit",
                    on_click=lambda: ClienteState.open_edit_customer_modal(customer),
                    class_name="text-blue-600 hover:underline ml-4",
                ),
            ),
            class_name="p-3 text-right",
        ),
    )


def cliente_modal() -> rx.Component:
    def form_field(label: str, name: str, value: str, placeholder: str, type: str = "text") -> rx.Component:
        return rx.el.div(
            rx.el.label(label, class_name="text-sm font-medium"),
            rx.el.input(
                placeholder=placeholder,
                name=name,
                type=type,
                default_value=value,
                on_change=lambda val: CustomerState.handle_customer_change(name, val),
                class_name="w-full p-2 border rounded-md mt-1",
            ),
        )

    return rx.cond(
        ClienteState.show_customer_modal,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            ClienteState.is_editing_customer,
                            "Edit Customer",
                            "Add New Customer",
                        ),
                        class_name="text-xl font-bold",
                    ),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=CustomerState.close_customer_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-center pb-4 border-b",
                ),
                rx.el.form(
                    rx.el.div(
                        form_field(
                            "Name",
                            "name",
                            CustomerState.new_customer["name"],
                            "e.g. John Doe",
                        ),
                        form_field(
                            "Email",
                            "email",
                            CustomerState.new_customer["email"],
                            "e.g. john@example.com",
                            type="email",
                        ),
                        form_field(
                            "Phone",
                            "phone",
                            CustomerState.new_customer["phone"],
                            "e.g. 123-456-7890",
                            type="tel",
                        ),
                        class_name="grid grid-cols-1 gap-4 py-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            on_click=CustomerState.close_customer_modal,
                            class_name="px-4 py-2 bg-gray-200 rounded-md",
                            type="button",
                        ),
                        rx.el.button(
                            "Save Customer",
                            type="submit",
                            class_name="px-4 py-2 bg-emerald-600 text-white rounded-md",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t",
                    ),
                    on_submit=CustomerState.save_customer,
                ),
                class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg",
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50",
        ),
    )


def cliente_page_ui() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Customers", class_name="text-3xl font-bold"),
            rx.el.p("Manage your customers here.", class_name="text-gray-500"),
            rx.el.button(
                "Add Customer",
                on_click=ClienteState.open_add_customer_modal,
                class_name="px-4 py-2 bg-emerald-600 text-white rounded-md mt-4",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Customer Info", class_name="p-3 text-left"),
                        rx.el.th("Contact", class_name="p-3 text-left"),
                        rx.el.th("Actions", class_name="p-3 text-right"),
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(rx.foreach(ClienteState.customers, cliente_list_item)),
            ),
            class_name="border rounded-lg overflow-hidden bg-white shadow",
        ),
        cliente_modal(),
    )