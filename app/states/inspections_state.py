import reflex as rx
from app.states.tire_management_state import TireManagementState
from app.states.base_state import Vehicle, VehicleTire, TireHistory
import datetime


class InspectionState(TireManagementState):
    show_inspection_modal: bool = False
    selected_vehicle_for_inspection: Vehicle | None = None
    current_inspection_tires: list[VehicleTire] = []
    inspection_depths: dict[str, str] = {}
    inspection_notes: str = ""

    @rx.event
    def open_inspection_modal(self, vehicle: Vehicle):
        self.selected_vehicle_for_inspection = vehicle
        self.current_inspection_tires = [
            vt for vt in self.vehicle_tires if vt["vehicle_id"] == vehicle["id"]
        ]
        self.inspection_depths = {
            str(vt["id"]): str(vt["profundidad_actual"])
            for vt in self.current_inspection_tires
        }
        self.inspection_notes = ""
        self.show_inspection_modal = True

    @rx.event
    def close_inspection_modal(self):
        self.show_inspection_modal = False
        self.selected_vehicle_for_inspection = None
        self.current_inspection_tires = []
        self.inspection_depths = {}
        self.inspection_notes = ""

    @rx.event
    def handle_depth_change(self, vehicle_tire_id: str, depth: str):
        self.inspection_depths[vehicle_tire_id] = depth

    @rx.event
    def save_inspection(self):
        if not self.selected_vehicle_for_inspection:
            return
        today = datetime.date.today().isoformat()
        for vt_id_str, new_depth_str in self.inspection_depths.items():
            try:
                vt_id = int(vt_id_str)
                new_depth = float(new_depth_str)
                vehicle_tire_index = next(
                    (i for i, vt in enumerate(self.vehicle_tires) if vt["id"] == vt_id),
                    -1,
                )
                if vehicle_tire_index == -1:
                    continue
                self.vehicle_tires[vehicle_tire_index]["profundidad_actual"] = new_depth
                if new_depth <= 1.03:
                    self.vehicle_tires[vehicle_tire_index]["estado"] = "Crítica"
                elif new_depth <= 3.0:
                    self.vehicle_tires[vehicle_tire_index]["estado"] = "Advertencia"
                else:
                    self.vehicle_tires[vehicle_tire_index]["estado"] = "En uso"
                new_history_id = (
                    max([th.get("id", 0) for th in self.tire_history] + [0]) + 1
                )
                history_entry: TireHistory = {
                    "id": new_history_id,
                    "vehicle_tire_id": vt_id,
                    "tipo_evento": "Inspeccion",
                    "fecha": today,
                    "notas": self.inspection_notes,
                    "profundidad_medida": new_depth,
                }
                self.tire_history.append(history_entry)
            except (ValueError, TypeError) as e:
                print(f"Error processing inspection data: {e}")
                #logging.exception
                continue
        self.close_inspection_modal()

    @rx.var
    def vehicles_for_inspection(self) -> list[Vehicle]:
        return self.vehicles