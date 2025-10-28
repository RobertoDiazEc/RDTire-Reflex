import reflex as rx
from app.states.base_state import BaseState, Tire, Sale, SaleItem, Customer
import datetime
from typing import TypedDict


class CartItem(TypedDict):
    tire: Tire
    quantity: int


class SalesState(BaseState):
    cart_items: list[CartItem] = []
    selected_customer_id: str = ""
    payment_method: str = "card"
    sales_history: list[Sale] = []
    filter_sale_date: str = ""

    @rx.event
    def add_to_cart(self, tire: Tire):
        for item in self.cart_items:
            if item["tire"]["id"] == tire["id"]:
                item["quantity"] += 1
                return
        self.cart_items.append({"tire": tire, "quantity": 1})

    @rx.event
    def remove_from_cart(self, tire_id: int):
        self.cart_items = [
            item for item in self.cart_items if item["tire"]["id"] != tire_id
        ]

    @rx.event
    def update_cart_quantity(self, tire_id: int, quantity: int):
        for item in self.cart_items:
            if item["tire"]["id"] == tire_id:
                if quantity > 0:
                    item["quantity"] = quantity
                else:
                    self.remove_from_cart(tire_id)
                return

    @rx.event
    def complete_sale(self):
        if not self.cart_items or not self.selected_customer_id:
            return
        new_sale_id = max([s["id"] for s in self.sales_history], default=0) + 1
        sale_items: list[SaleItem] = []
        for item in self.cart_items:
            tire_id = item["tire"]["id"]
            quantity = item["quantity"]
            for i, tire_in_stock in enumerate(self.tires):
                if tire_in_stock["id"] == tire_id:
                    if self.tires[i]["stock"] >= quantity:
                        self.tires[i]["stock"] -= quantity
                        sale_items.append(
                            {
                                "tire_id": tire_id,
                                "quantity": quantity,
                                "price_at_sale": item["tire"]["price"],
                            }
                        )
                    else:
                        return
                    break
        new_sale = {
            "id": new_sale_id,
            "timestamp": datetime.datetime.now().isoformat(),
            "customer_id": int(self.selected_customer_id),
            "items": sale_items,
            "total": self.cart_total,
            "payment_method": self.payment_method,
        }
        self.sales_history.insert(0, new_sale)
        self.cart_items = []

    @rx.var
    def cart_subtotal(self) -> float:
        return sum(
            (item["tire"]["price"] * item["quantity"] for item in self.cart_items)
        )

    @rx.var
    def cart_tax(self) -> float:
        return self.cart_subtotal * 0.1

    @rx.var
    def cart_total(self) -> float:
        return self.cart_subtotal + self.cart_tax

    @rx.var
    def filtered_sales_history(self) -> list[Sale]:
        if not self.filter_sale_date:
            return self.sales_history
        return [
            s
            for s in self.sales_history
            if s["timestamp"].startswith(self.filter_sale_date)
        ]

    @rx.event
    def get_tire_from_id(self, tire_id: int) -> Tire | None:
        for tire in self.tires:
            if tire["id"] == tire_id:
                return tire
        return None

    @rx.event
    def get_customer_from_id(self, customer_id: int) -> Customer | None:
        for customer in self.customers:
            if customer["id"] == customer_id:
                return customer
        return None