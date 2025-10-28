import reflex as rx
from app.states.base_state import BaseState, Tire
import datetime
import logging


class InventoryState(BaseState):
    show_adjustment_modal: bool = False
    selected_tire_for_adjustment: Tire | None = None
    adjustment_amount: str = "0"
    adjustment_reason: str = ""

    @rx.event
    def open_inventory_adjustment_modal(self, tire: Tire):
        self.selected_tire_for_adjustment = tire
        self.show_adjustment_modal = True
        self.adjustment_amount = "0"
        self.adjustment_reason = ""

    @rx.event
    def close_inventory_adjustment_modal(self):
        self.show_adjustment_modal = False
        self.selected_tire_for_adjustment = None

    @rx.event
    def save_inventory_adjustment(self):
        if self.selected_tire_for_adjustment and self.adjustment_amount:
            try:
                amount = int(self.adjustment_amount)
                tire_id = self.selected_tire_for_adjustment["id"]
                for i, tire in enumerate(self.tires):
                    if tire["id"] == tire_id:
                        self.tires[i]["stock"] += amount
                        new_adjustment = {
                            "timestamp": datetime.datetime.now().isoformat(),
                            "reason": self.adjustment_reason or "Manual Adjustment",
                            "amount": amount,
                        }
                        if "inventory_history" not in self.tires[i]:
                            self.tires[i]["inventory_history"] = []
                        self.tires[i]["inventory_history"].append(new_adjustment)
                        break
                self.close_inventory_adjustment_modal()
            except ValueError as e:
                logging.exception(f"Error converting adjustment_amount: {e}")

    @rx.var
    def low_stock_tires(self) -> list[Tire]:
        return [t for t in self.tires if t["stock"] < 10]