import reflex as rx
from app.states.inventory_state import InventoryState, Tire


def inventory_table() -> rx.Component:
    def stock_badge(stock: int) -> rx.Component:
        return rx.cond(
            stock < 10,
            rx.el.span(
                "Low Stock",
                class_name="px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full w-fit",
            ),
            rx.el.span(
                f"{stock} in stock",
                class_name="px-2 py-1 text-xs font-semibold text-emerald-800 bg-emerald-100 rounded-full w-fit",
            ),
        )

    return rx.box(
        rx.box(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("Product", class_name="p-3 text-left"),
                        rx.el.th("Stock Level", class_name="p-3 text-left"),
                        rx.el.th("Status", class_name="p-3 text-left"),
                        rx.el.th("Actions", class_name="p-3 text-right"),
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        InventoryState.filtered_tires,
                        lambda tire: rx.el.tr(
                            rx.el.td(
                                rx.box(
                                    rx.el.p(
                                        f"{tire['brand']} {tire['model']}",
                                        class_name="font-medium",
                                    ),
                                    rx.el.p(
                                        tire["size"], class_name="text-sm text-gray-500"
                                    ),
                                    class_name="flex flex-col",
                                ),
                                class_name="p-3",
                            ),
                            rx.el.td(stock_badge(tire["stock"]), class_name="p-3"),
                            rx.el.td(
                                rx.cond(
                                    tire["stock"] < 10,
                                    "Requires attention",
                                    "Sufficient",
                                ),
                                class_name="p-3",
                            ),
                            rx.el.td(
                                rx.el.button(
                                    "Adjust Stock",
                                    on_click=lambda: InventoryState.open_inventory_adjustment_modal(
                                        tire
                                    ),
                                    class_name="bg-gray-200 text-gray-800 px-3 py-1 rounded-md text-sm hover:bg-gray-300",
                                ),
                                class_name="p-3 text-right",
                            ),
                        ),
                    )
                ),
            ),
            class_name="border rounded-lg overflow-hidden",
        ),
        class_name="bg-white p-6 rounded-lg shadow",
    )


def adjustment_modal() -> rx.Component:
    return rx.cond(
        InventoryState.show_adjustment_modal,
        rx.box(
            rx.box(
                rx.box(
                    rx.el.h2("Adjust Inventory", class_name="text-xl font-bold"),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=InventoryState.close_inventory_adjustment_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-center pb-4 border-b",
                ),
                rx.cond(
                    InventoryState.selected_tire_for_adjustment != None,
                    rx.box(
                        rx.el.p(
                            f"Adjusting stock for: {InventoryState.selected_tire_for_adjustment['brand']} {InventoryState.selected_tire_for_adjustment['model']}",
                            class_name="font-medium mb-4",
                        ),
                        # rx.box(
                        #     rx.el.label(
                        #         "Adjustment Amount (negative to decrease)",
                        #         class_name="text-sm font-medium",
                        #     ),
                        #     rx.input(
                        #         default_value=InventoryState.adjustment_amount,
                        #         on_change=InventoryState.set_adjustment_amount,
                        #         type="number",
                        #         class_name="w-full p-2 border rounded-md mt-1",
                        #     ),
                        #     class_name="mb-4",
                        # ),
                        # rx.box(
                        #     rx.el.label(
                        #         "Reason for Adjustment",
                        #         class_name="text-sm font-medium",
                        #     ),
                        #     rx.input(
                        #         default_value=InventoryState.adjustment_reason,
                        #         on_change=InventoryState.set_adjustment_reason,
                        #         placeholder="e.g. Received new shipment, Stock count correction",
                        #         class_name="w-full p-2 border rounded-md mt-1",
                        #     ),
                        #     class_name="mb-4",
                        # ),
                        class_name="py-4",
                    ),
                ),
                rx.box(
                    rx.button(
                        "Cancel",
                        on_click=InventoryState.close_inventory_adjustment_modal,
                        class_name="px-4 py-2 bg-gray-200 rounded-md",
                    ),
                    rx.button(
                        "Save Adjustment",
                        on_click=InventoryState.save_inventory_adjustment,
                        class_name="px-4 py-2 bg-emerald-600 text-white rounded-md",
                    ),
                    class_name="flex justify-end gap-2 pt-4 border-t",
                ),
                class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg",
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50",
        ),
    )


def inventory_page_ui() -> rx.Component:
    return rx.box(
        rx.el.h1("Inventory Management", class_name="text-3xl font-bold mb-6"),
        inventory_table(),
        adjustment_modal(),
    )