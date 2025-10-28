import reflex as rx
from app.states.base_state import BaseState, Vehicle, VehicleTire, TireHistory
import datetime
import logging
from typing import cast


class VehicleState(BaseState):
    show_vehicle_modal: bool = False
    is_editing_vehicle: bool = False
    selected_vehicle: Vehicle | None = None
    new_vehicle: Vehicle = {
        "id": 0,
        "placa": "",
        "marca": "",
        "modelo": "",
        "ano": 2024,
        "tipo": "",
        "fecha_registro": "",
    }

    @rx.event
    def open_add_vehicle_modal(self):
        self.is_editing_vehicle = False
        self.new_vehicle = {
            "id": 0,
            "placa": "",
            "marca": "",
            "modelo": "",
            "ano": datetime.date.today().year,
            "tipo": "",
            "fecha_registro": "",
        }
        self.show_vehicle_modal = True

    @rx.event
    def open_edit_vehicle_modal(self, vehicle: Vehicle):
        self.is_editing_vehicle = True
        self.selected_vehicle = vehicle
        self.new_vehicle = vehicle.copy()
        self.show_vehicle_modal = True

    @rx.event
    def close_vehicle_modal(self):
        self.show_vehicle_modal = False
        self.selected_vehicle = None
        self.is_editing_vehicle = False

    @rx.event
    def handle_vehicle_change(self, field: str, value: str):
        if field == "ano":
            try:
                self.new_vehicle[field] = int(value)
            except ValueError as e:
                logging.exception(f"Error converting ano to int: {e}")
        else:
            self.new_vehicle[field] = value

    @rx.event
    def save_vehicle(self):
        if self.is_editing_vehicle and self.selected_vehicle:
            vehicle_index = next(
                (
                    i
                    for i, v in enumerate(self.vehicles)
                    if v["id"] == self.selected_vehicle["id"]
                ),
                -1,
            )
            if vehicle_index != -1:
                self.vehicles[vehicle_index] = self.new_vehicle.copy()
        else:
            new_id = max([v["id"] for v in self.vehicles]) + 1 if self.vehicles else 1
            self.new_vehicle["id"] = new_id
            self.new_vehicle["fecha_registro"] = datetime.date.today().isoformat()
            self.vehicles.append(self.new_vehicle.copy())
        self.close_vehicle_modal()

    @rx.event
    def delete_vehicle(self, vehicle_id: int):
        self.vehicles = [v for v in self.vehicles if v["id"] != vehicle_id]
        self.vehicle_tires = [
            vt for vt in self.vehicle_tires if vt["vehicle_id"] != vehicle_id
        ]