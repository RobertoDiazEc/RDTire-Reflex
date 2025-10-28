import reflex as rx
from app.states.sales_state import SalesState, Sale
from datetime import datetime
import csv
import io


class ReportsState(SalesState):
    report_start_date: str = ""
    report_end_date: str = ""

    @rx.event
    def set_report_start_date(self, date: str):
        self.report_start_date = date

    @rx.event
    def set_report_end_date(self, date: str):
        self.report_end_date = date

    @rx.var
    def filtered_sales(self) -> list[Sale]:
        sales = self.sales_history
        if self.report_start_date:
            start_date = datetime.fromisoformat(self.report_start_date + "T00:00:00")
            sales = [
                s for s in sales if datetime.fromisoformat(s["timestamp"]) >= start_date
            ]
        if self.report_end_date:
            end_date = datetime.fromisoformat(self.report_end_date + "T23:59:59")
            sales = [
                s for s in sales if datetime.fromisoformat(s["timestamp"]) <= end_date
            ]
        return sales

    @rx.var
    def revenue_by_category(self) -> list[dict[str, str | float]]:
        category_revenue = {t_type: 0.0 for t_type in self.unique_types}
        for sale in self.filtered_sales:
            for item in sale["items"]:
                for tire in self.tires:
                    if tire["id"] == item["tire_id"]:
                        category_revenue[tire["type"]] += (
                            item["price_at_sale"] * item["quantity"]
                        )
                        break
        return [
            {"category": cat, "revenue": rev} for cat, rev in category_revenue.items()
        ]

    @rx.event
    def export_sales_csv(self) -> rx.event.EventSpec:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Sale ID", "Timestamp", "Customer", "Total", "Payment Method"])
        for sale in self.filtered_sales:
            customer_name = "N/A"
            for c in self.customers:
                if c["id"] == sale["customer_id"]:
                    customer_name = c["name"]
                    break
            writer.writerow(
                [
                    sale["id"],
                    sale["timestamp"],
                    customer_name,
                    sale["total"],
                    sale["payment_method"],
                ]
            )
        csv_data = output.getvalue()
        return rx.download(data=csv_data.encode("utf-8"), filename="sales_report.csv")