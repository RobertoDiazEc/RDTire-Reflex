import reflex as rx
from app.states.base_state import BaseState, Customer
import logging


class CustomerState(BaseState):
    show_customer_modal: bool = False
    is_editing_customer: bool = False
    selected_customer: Customer | None = None
    new_customer: Customer = {"id": 0, "name": "", "email": "", "phone": ""}

    @rx.event
    def open_add_customer_modal(self):
        self.is_editing_customer = False
        self.new_customer = {"id": 0, "name": "", "email": "", "phone": ""}
        self.show_customer_modal = True

    @rx.event
    def open_edit_customer_modal(self, customer: Customer):
        self.is_editing_customer = True
        self.selected_customer = customer
        self.new_customer = customer.copy()
        self.show_customer_modal = True

    @rx.event
    def close_customer_modal(self):
        self.show_customer_modal = False
        self.selected_customer = None
        self.is_editing_customer = False

    @rx.event
    def handle_customer_change(self, field: str, value: str):
        self.new_customer[field] = value

    @rx.event
    def save_customer(self, form_data: dict):
        if self.is_editing_customer and self.selected_customer:
            customer_index = next(
                (
                    i
                    for i, c in enumerate(self.customers)
                    if c["id"] == self.selected_customer["id"]
                ),
                -1,
            )
            if customer_index != -1:
                self.customers[customer_index]["name"] = self.new_customer["name"]
                self.customers[customer_index]["email"] = self.new_customer["email"]
                self.customers[customer_index]["phone"] = self.new_customer["phone"]
        else:
            new_id = max([c["id"] for c in self.customers]) + 1 if self.customers else 1
            self.new_customer["id"] = new_id
            self.customers.append(self.new_customer.copy())
        self.close_customer_modal()