import reflex as rx
from app.states.sales_state import SalesState
from collections import defaultdict
from datetime import datetime, timedelta


class AnalyticsState(SalesState):
    time_range: str = "daily"

    @rx.var
    def total_revenue(self) -> float:
        return sum((s["total"] for s in self.sales_history))

    @rx.var
    def total_sales(self) -> int:
        return len(self.sales_history)

    @rx.var
    def average_sale_value(self) -> float:
        if not self.sales_history:
            return 0
        return self.total_revenue / self.total_sales

    @rx.var
    def total_inventory_value(self) -> float:
        return sum((t.price * t.stock for t in self.tires))

    @rx.var
    def sales_chart_data(self) -> list[dict[str, float | str]]:
        sales_by_date = defaultdict(float)
        now = datetime.now()
        for sale in self.sales_history:
            sale_date = datetime.fromisoformat(sale["timestamp"])
            if self.time_range == "daily":
                if now - sale_date > timedelta(days=30):
                    continue
                date_key = sale_date.strftime("%Y-%m-%d")
            elif self.time_range == "weekly":
                if now - sale_date > timedelta(weeks=26):
                    continue
                date_key = sale_date.strftime("%Y-W%W")
            else:
                if now - sale_date > timedelta(days=365 * 2):
                    continue
                date_key = sale_date.strftime("%Y-%m")
            sales_by_date[date_key] += sale["total"]
        sorted_dates = sorted(sales_by_date.keys())
        return [{"date": date, "sales": sales_by_date[date]} for date in sorted_dates]

    @rx.var
    def top_selling_products(self) -> list[dict[str, str | int]]:
        product_sales = defaultdict(int)
        for sale in self.sales_history:
            for item in sale["items"]:
                product_sales[item["tire_id"]] += item["quantity"]
        sorted_products = sorted(
            product_sales.items(), key=lambda x: x[1], reverse=True
        )[:5]
        top_products = []
        for tire_id, quantity in sorted_products:
            for tire in self.tires:
                if tire["id"] == tire_id:
                    top_products.append(
                        {
                            "name": f"{tire['brand']} {tire['model']}",
                            "quantity": quantity,
                        }
                    )
                    break
        return top_products

    @rx.var
    def sales_by_category(self) -> list[dict[str, str | int]]:
        category_sales = defaultdict(int)
        for sale in self.sales_history:
            for item in sale["items"]:
                for tire in self.tires:
                    if tire["id"] == item["tire_id"]:
                        category_sales[tire["type"]] += item["quantity"]
                        break
        return [{"name": cat, "value": val} for cat, val in category_sales.items()]

    @rx.event
    def set_time_range(self, range: str):
        self.time_range = range