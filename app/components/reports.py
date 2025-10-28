import reflex as rx
from app.states.reports_state import ReportsState


def reports_page_ui() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Reports", class_name="text-3xl font-bold"),
            rx.el.p(
                "Generate and export business reports.", class_name="text-gray-500"
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.h2("Sales Report", class_name="text-xl font-semibold"),
            rx.el.div(
                rx.el.div(
                    rx.el.label("Start Date"),
                    rx.el.input(
                        type="date",
                        on_change=ReportsState.set_report_start_date,
                        class_name="p-2 border rounded-md",
                    ),
                ),
                rx.el.div(
                    rx.el.label("End Date"),
                    rx.el.input(
                        type="date",
                        on_change=ReportsState.set_report_end_date,
                        class_name="p-2 border rounded-md",
                    ),
                ),
                rx.el.button(
                    "Export CSV",
                    on_click=ReportsState.export_sales_csv,
                    class_name="px-4 py-2 bg-emerald-600 text-white rounded-md self-end",
                ),
                class_name="flex items-center gap-4 p-4 border rounded-lg bg-gray-50 mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th("Sale ID"),
                            rx.el.th("Timestamp"),
                            rx.el.th("Customer"),
                            rx.el.th("Total"),
                            rx.el.th("Payment Method"),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            ReportsState.filtered_sales,
                            lambda sale: rx.el.tr(
                                rx.el.td(sale["id"]),
                                rx.el.td(sale["timestamp"]),
                                rx.el.td(
                                    rx.foreach(
                                        ReportsState.customers,
                                        lambda customer: rx.cond(
                                            customer["id"] == sale["customer_id"],
                                            rx.el.span(customer["name"]),
                                            None,
                                        ),
                                    )
                                ),
                                rx.el.td(f"${sale['total']:.2f}"),
                                rx.el.td(sale["payment_method"]),
                            ),
                        )
                    ),
                    class_name="w-full text-left",
                ),
                class_name="bg-white p-6 rounded-lg shadow overflow-x-auto",
            ),
            class_name="space-y-4",
        ),
    )