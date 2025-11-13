import reflex as rx
from app.states.base_state import BaseState, Tire
from app.states.auth_state import AuthState

# , **props
def product_card(tire: Tire) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=tire["image_url"], class_name="aspect-square w-full object-cover"
            ),
            class_name="overflow-hidden rounded-t-lg",
        ),
        rx.el.div(
            rx.el.h3(tire["brand"], class_name="text-lg font-bold"),
            rx.el.p(tire["model"], class_name="text-sm text-gray-500"),
            rx.el.p(tire["dot"], class_name="text-sm text-gray-500"),
            rx.el.div(
                rx.el.p(f"${tire['price']:.2f}", class_name="text-lg font-semibold"),
                rx.el.p(f"Stock: {tire['stock']}", class_name="text-sm text-gray-600"),
                class_name="flex items-center justify-between mt-2",
            ),
            class_name="p-4 bg-white",
        ),
        on_click=lambda: BaseState.open_product_detail_modal(tire),
        class_name="rounded-lg border border-gray-200 bg-white shadow-sm hover:shadow-lg transition-shadow cursor-pointer flex flex-col justify-between",
        #**props,
    )


def products_page_ui() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            #rx.el.h1("Products", class_name="text-3xl font-bold"),
            rx.el.p(
                "Ingreso de Neumaticos .", class_name="text-gray-500 mt-1"
            ),
            rx.el.button(
                "Nuevo",
                on_click=BaseState.open_add_product_modal(AuthState.current_user["cliente_id"]),
                class_name="mt-4 bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700",
            ),
            rx.button(
                rx.icon("table-cells-split", size=20),
                rx.text("Mostrar", size="3"),
                on_click=BaseState.mostrar_tires(AuthState.current_user["cliente_id"]),
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            # BaseState.filtered_tires
            rx.foreach(BaseState.tires, product_card),
            class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6",
        ),
        #product_detail_modal(),
        add_product_modal(),
        class_name="p-4 md:p-6",
    )


def product_detail_modal() -> rx.Component:
    return rx.cond(
        BaseState.show_product_detail_modal & (BaseState.selected_tire != None),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        f"{BaseState.selected_tire['brand']} {BaseState.selected_tire['size']}",
                        class_name="text-2xl font-bold",
                    ),
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=BaseState.close_product_detail_modal,
                        class_name="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none",
                    ),
                    class_name="flex items-center justify-between",
                ),
                rx.el.div(
                    rx.image(
                        src=BaseState.selected_tire["image_url"],
                        class_name="w-full h-64 object-cover rounded-lg",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p("model:", class_name="font-semibold"),
                            rx.el.p(BaseState.selected_tire["size"]),
                        ),
                        rx.el.div(
                            rx.el.p("Type:", class_name="font-semibold"),
                            rx.el.p(BaseState.selected_tire["type"]),
                        ),
                        rx.el.div(
                            rx.el.p("Season:", class_name="font-semibold"),
                            rx.el.p(BaseState.selected_tire["season"]),
                        ),
                        rx.el.div(
                            rx.el.p("Speed Rating:", class_name="font-semibold"),
                            rx.el.p(BaseState.selected_tire["speed_rating"]),
                        ),
                        rx.el.div(
                            rx.el.p("Load Index:", class_name="font-semibold"),
                            rx.el.p(BaseState.selected_tire["load_index"]),
                        ),
                        class_name="grid grid-cols-2 gap-4 text-sm mt-4",
                    ),
                    class_name="grid md:grid-cols-2 gap-6 mt-4",
                ),
                rx.el.div(
                    rx.el.p(
                        f"${BaseState.selected_tire['price']:.2f}",
                        class_name="text-3xl font-bold",
                    ),
                    rx.el.p(
                        f"In Stock: {BaseState.selected_tire['stock']}",
                        class_name="text-emerald-600 font-semibold",
                    ),
                    class_name="flex items-center justify-between mt-6",
                ),
                class_name="relative bg-white p-6 rounded-lg shadow-lg w-full max-w-2xl",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/50",
        ),
        None,
    )


def add_product_modal() -> rx.Component:
    def form_field(
        label: str, name: str, placeholder: str, type: str = "text"
    ) -> rx.Component:
        return rx.el.div(
            rx.el.label(label, class_name="text-sm font-medium"),
            rx.el.input(
                placeholder=placeholder,
                name=name,
                type=type,
                on_change=lambda val: BaseState.handle_new_product_change(name, val),
                class_name="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
            ),
            class_name="space-y-1.5",
        )

    return rx.cond(
        BaseState.show_add_product_modal,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2("Nuevo", class_name="text-xl font-bold"),
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        on_click=BaseState.close_add_product_modal,
                        class_name="rounded-sm opacity-70 ring-offset-background transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:pointer-events-none",
                    ),
                    class_name="flex items-center justify-between pb-4 border-b",
                ),
                rx.el.form(
                    rx.el.div(
                        form_field("Marca", "brand", "e.g. Michelin"),
                        form_field("Medida", "size", "e.g. 255/35R19"),
                        form_field("DOT", "dot", "e.g. 1421"),
                        form_field("Modelo", "model", "e.g. Pilot Sport 4S"),
                        form_field("Type", "type", "e.g. Performance"),
                        form_field("Season", "season", "e.g. Summer"),
                        form_field("Speed Rating", "speed_rating", "e.g. Y"),
                        form_field("Load Index", "load_index", "e.g. 96"),
                        form_field("Price", "price", "e.g. 350.00", type="number"),
                        form_field("Stock", "stock", "e.g. 50", type="number"),
                        form_field(
                            "Image URL", "image_url", "e.g. https://.../image.png"
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 py-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=BaseState.close_add_product_modal,
                            class_name="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg hover:bg-gray-200",
                        ),
                        rx.el.button(
                            "Grabar",
                            type="submit",
                            class_name="bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t",
                    ),
                    on_submit=BaseState.save_new_product,
                ),
                class_name="relative bg-white p-6 rounded-lg shadow-lg w-full max-w-4xl",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center bg-black/50",
        ),
        None,
    )