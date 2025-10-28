import reflex as rx
from app.states.sales_state import SalesState


def product_selector_card(tire: dict) -> rx.Component:
    return rx.el.div(
        rx.image(
            src=tire["image_url"], class_name="w-full h-32 object-cover rounded-t-lg"
        ),
        rx.el.div(
            rx.el.p(f"{tire['brand']} {tire['model']}", class_name="font-semibold"),
            rx.el.p(f"${tire['price']:.2f}", class_name="text-gray-700"),
            rx.el.p(f"Stock: {tire['stock']}", class_name="text-sm text-gray-500"),
            class_name="p-3",
        ),
        on_click=lambda: SalesState.add_to_cart(tire),
        class_name="border rounded-lg cursor-pointer hover:shadow-md transition-shadow",
    )


def shopping_cart_item(item: dict) -> rx.Component:
    tire = item["tire"]
    return rx.el.div(
        rx.el.div(
            rx.el.p(f"{tire['brand']} {tire['model']}", class_name="font-semibold"),
            rx.el.p(f"${tire['price']:.2f}", class_name="text-sm text-gray-600"),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.input(
                on_change=lambda qty: SalesState.update_cart_quantity(
                    tire["id"], qty.to(int)
                ),
                type="number",
                class_name="w-16 p-1 border rounded-md text-center",
                default_value=item["quantity"].to_string(),
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.p(
            f"${item['quantity'] * tire['price']:.2f}",
            class_name="font-semibold w-20 text-right",
        ),
        rx.el.button(
            rx.icon("trash-2", class_name="h-4 w-4"),
            on_click=lambda: SalesState.remove_from_cart(tire["id"]),
            class_name="text-gray-500 hover:text-red-500",
        ),
        class_name="flex items-center gap-4 py-3 border-b",
    )


def sales_page_ui() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h2("Product Selection", class_name="text-2xl font-bold mb-4"),
                rx.el.div(
                    rx.foreach(SalesState.filtered_tires, product_selector_card),
                    class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 overflow-y-auto max-h-[80vh] p-1",
                ),
                class_name="bg-white p-6 rounded-lg shadow",
            ),
            class_name="flex-grow",
        ),
        rx.el.aside(
            rx.el.div(
                rx.el.h2("Shopping Cart", class_name="text-2xl font-bold mb-4"),
                rx.el.div(
                    rx.cond(
                        SalesState.cart_items.length() > 0,
                        rx.foreach(SalesState.cart_items, shopping_cart_item),
                        rx.el.div(
                            "Cart is empty",
                            class_name="text-center text-gray-500 py-10",
                        ),
                    ),
                    class_name="flex-grow overflow-y-auto max-h-[40vh] pr-2",
                ),
                rx.cond(
                    SalesState.cart_items.length() > 0,
                    rx.el.div(
                        rx.el.div(
                            rx.el.div("Subtotal", class_name="font-medium"),
                            rx.el.div(f"${SalesState.cart_subtotal:.2f}"),
                            class_name="flex justify-between py-1",
                        ),
                        rx.el.div(
                            rx.el.div("Tax (10%)", class_name="font-medium"),
                            rx.el.div(f"${SalesState.cart_tax:.2f}"),
                            class_name="flex justify-between py-1",
                        ),
                        rx.el.div(
                            rx.el.div("Total", class_name="font-bold text-lg"),
                            rx.el.div(
                                f"${SalesState.cart_total:.2f}",
                                class_name="font-bold text-lg",
                            ),
                            class_name="flex justify-between py-2 border-t",
                        ),
                        rx.el.div(
                            rx.el.label("Customer", class_name="font-medium"),
                            rx.el.select(
                                rx.el.option(
                                    "Select Customer", value="", disabled=True
                                ),
                                rx.foreach(
                                    SalesState.customers,
                                    lambda c: rx.el.option(
                                        c["name"], value=c["id"].to_string()
                                    ),
                                ),
                                on_change=SalesState.set_selected_customer_id,
                                class_name="w-full p-2 border rounded-md mt-1",
                            ),
                            class_name="mt-4",
                        ),
                        rx.el.div(
                            rx.el.label("Payment Method", class_name="font-medium"),
                            rx.el.select(
                                rx.el.option("Card", value="card"),
                                rx.el.option("Cash", value="cash"),
                                rx.el.option("Credit", value="credit"),
                                on_change=SalesState.set_payment_method,
                                class_name="w-full p-2 border rounded-md mt-1",
                            ),
                            class_name="mt-4",
                        ),
                        rx.el.button(
                            "Complete Sale",
                            on_click=SalesState.complete_sale,
                            class_name="w-full bg-emerald-600 text-white p-3 rounded-lg mt-6 font-bold hover:bg-emerald-700",
                            disabled=(SalesState.cart_items.length() == 0)
                            | (SalesState.selected_customer_id == ""),
                        ),
                        class_name="mt-auto",
                    ),
                ),
                class_name="bg-white p-6 rounded-lg shadow flex flex-col h-full",
            ),
            class_name="w-full lg:w-[450px] shrink-0",
        ),
        class_name="flex flex-col lg:flex-row gap-6",
    )