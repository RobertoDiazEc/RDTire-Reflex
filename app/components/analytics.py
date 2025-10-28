import reflex as rx
from app.states.analytics_state import AnalyticsState


def metric_card(title: str, value: rx.Var | str, icon: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name="h-6 w-6 text-gray-500"),
            class_name="p-2 bg-gray-100 rounded-md",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.p(value, class_name="text-2xl font-bold"),
            class_name="flex flex-col",
        ),
        class_name="flex items-center gap-4 p-4 bg-white rounded-lg shadow",
    )


def analytics_dashboard() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Analytics Dashboard", class_name="text-3xl font-bold"),
            rx.el.p(
                "Insights into your business performance.", class_name="text-gray-500"
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            metric_card(
                "Total Revenue", f"${AnalyticsState.total_revenue:.2f}", "dollar-sign"
            ),
            metric_card(
                "Total Sales", AnalyticsState.total_sales.to_string(), "shopping-cart"
            ),
            metric_card(
                "Avg. Sale Value",
                f"${AnalyticsState.average_sale_value:.2f}",
                "bar-chart-2",
            ),
            metric_card(
                "Inventory Value",
                f"${AnalyticsState.total_inventory_value:.2f}",
                "boxes",
            ),
            class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h2("Sales Trends", class_name="text-xl font-semibold mb-4"),
                rx.el.div(
                    rx.el.button(
                        "Daily",
                        on_click=lambda: AnalyticsState.set_time_range("daily"),
                        class_name=rx.cond(
                            AnalyticsState.time_range == "daily",
                            "bg-emerald-600 text-white",
                            "bg-gray-200",
                        ),
                    ),
                    rx.el.button(
                        "Weekly",
                        on_click=lambda: AnalyticsState.set_time_range("weekly"),
                        class_name=rx.cond(
                            AnalyticsState.time_range == "weekly",
                            "bg-emerald-600 text-white",
                            "bg-gray-200",
                        ),
                    ),
                    rx.el.button(
                        "Monthly",
                        on_click=lambda: AnalyticsState.set_time_range("monthly"),
                        class_name=rx.cond(
                            AnalyticsState.time_range == "monthly",
                            "bg-emerald-600 text-white",
                            "bg-gray-200",
                        ),
                    ),
                    class_name="flex gap-2 mb-4",
                ),
                rx.recharts.line_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.x_axis(data_key="date"),
                    rx.recharts.y_axis(),
                    rx.recharts.line(
                        data_key="sales", stroke="#10b981", active_dot={"r": 8}
                    ),
                    data=AnalyticsState.sales_chart_data,
                    height=300,
                ),
                class_name="bg-white p-6 rounded-lg shadow",
            ),
            rx.el.div(
                rx.el.h2(
                    "Top Selling Products", class_name="text-xl font-semibold mb-4"
                ),
                rx.recharts.bar_chart(
                    rx.recharts.cartesian_grid(stroke_dasharray="3 3"),
                    rx.recharts.graphing_tooltip(),
                    rx.recharts.x_axis(data_key="name"),
                    rx.recharts.y_axis(),
                    rx.recharts.bar(data_key="quantity", fill="#10b981"),
                    data=AnalyticsState.top_selling_products,
                    layout="vertical",
                    height=300,
                ),
                class_name="bg-white p-6 rounded-lg shadow",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-6",
        ),
    )