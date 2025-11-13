import reflex as rx
from app.states.vehicle_state import VehicleState
from app.database.db_rdtire import Vehiculo as Vehicle, VehicleTire, TireHistory, Tire
import datetime
from typing import cast, List


class TireManagementState(VehicleState):
    show_vehicle_detail_modal: bool = False
    selected_vehicle_for_detail: List[Vehicle] = []
    show_add_tire_modal: bool = False
    show_tire_history_modal: bool = False
    selected_vehicle_tire: VehicleTire | None = None
    new_vehicle_tire: VehicleTire = VehicleTire()
    tires_all_options: List[str] = []

    #Obtengo informacion del vehiculo seleccionado
    @rx.event
    def open_vehicle_detail(self, vehicle_id: int):
        print(f" vehicle id en state {vehicle_id}")
        if vehicle_id is None:
            return rx.window_alert(" vehicle id es none ")
        self.selected_vehicle_for_detail = []
        with rx.session() as session:
            vehiculo_seleccion = session.exec(
                               Vehicle.select().where(
                                    Vehicle.id == vehicle_id
                                )
                            ).all()
            for seleccion in vehiculo_seleccion:
                nuevo_registro = {
                        "id": seleccion.id,
                        "cliente_id": seleccion.cliente_id,
                        "marca": seleccion.marca,
                        "modelo": seleccion.modelo,
                        "anio": seleccion.anio,
                        "placa": seleccion.placa,
                        "tipo": seleccion.tipo,
                       }
                self.selected_vehicle_for_detail.append(nuevo_registro) 
                      #  = next(
        #     (v for v in self.vehicles if v["id"] == vehicle_id), None
        # )
        self.show_vehicle_detail_modal = True

    @rx.event
    def close_vehicle_detail(self):
        self.show_vehicle_detail_modal = False
        self.selected_vehicle_for_detail = None

    @rx.event
    def open_add_tire_to_vehicle_modal(self, vehicle_id: int, cliente_id: int, position: str):
        self.new_vehicle_tire = {
            "id": 0,
            "vehicle_id": vehicle_id,
            "tire_id": self.tires.id if self.tires else 0,
            "position": position,
            "fecha_instalacion": datetime.date.today().isoformat(),
            "estado": "Nueva",
            "profundidad_actual": 8.0,
        }
        #buscar todas las tires y almacenar en variable
        with rx.session() as session:
            tires_data = session.exec(
                               Tire.select().where(
                                    Tire.cliente_id == cliente_id and Tire.asignado_a_vehiculo == False
                                )
                            ).all()
            self.tires_all_options = [f"{tire.id} - {tire.brand} {tire.model} {tire.size}" for tire in tires_data]  
            
        self.show_add_tire_modal = True

    @rx.event
    def close_add_tire_to_vehicle_modal(self):
        self.show_add_tire_modal = False

    @rx.event
    def handle_new_vehicle_tire_change(self, field: str, value: str):
        print(value.split(" - ")[-1])
        if field in ["tire_id", "vehicle_id"]:
            self.new_vehicle_tire[field] = int(value.split(" - ")[0])
        elif field == "profundidad_actual":
            self.new_vehicle_tire[field] = float(value)
        else:
            self.new_vehicle_tire[field] = value

    @rx.event
    def save_tire_to_vehicle(self, form_data: dict):
        for field, value in form_data.items():
            self.handle_new_vehicle_tire_change(field, value)
        new_id = max([vt["id"] for vt in self.vehicle_tires] + [0]) + 1
        self.new_vehicle_tire["id"] = new_id
        self.vehicle_tires.append(self.new_vehicle_tire.copy())
        new_history_id = max([th["id"] for th in self.tire_history] + [0]) + 1
        history_entry: TireHistory = {
            "id": new_history_id,
            "vehicle_tire_id": new_id,
            "tipo_evento": "Instalacion",
            "fecha": self.new_vehicle_tire["fecha_instalacion"],
            "notas": f"Llanta nueva instalada con profundidad de {self.new_vehicle_tire['profundidad_actual']}mm",
            "profundidad_medida": self.new_vehicle_tire["profundidad_actual"],
        }
        self.tire_history.append(history_entry)
        self.show_add_tire_modal = False

    @rx.event
    def change_value_tires(self, value: str):
        self.new_vehicle_tire["tire_id"] = int(value.split(" - ")[-1])

    @rx.event
    def remove_tire_from_vehicle(self, vehicle_tire_id: int):
        tire_index = next(
            (
                i
                for i, vt in enumerate(self.vehicle_tires)
                if vt["id"] == vehicle_tire_id
            ),
            -1,
        )
        if tire_index != -1:
            self.vehicle_tires.pop(tire_index)

    @rx.event
    def open_tire_history_modal(self, vehicle_tire_id: int):
        self.selected_vehicle_tire = next(
            (vt for vt in self.vehicle_tires if vt["id"] == vehicle_tire_id), None
        )
        self.show_tire_history_modal = True

    @rx.event
    def close_tire_history_modal(self):
        self.show_tire_history_modal = False
        self.selected_vehicle_tire = None

    @rx.event
    def posicion_llanta_imagen(self, position: str) -> str:
        if not self.selected_vehicle_for_detail:
            return ""
        vehicle_id = self.selected_vehicle_for_detail[0]["id"]
        tires_s = {
            vt["position"]: vt
            for vt in self.vehicle_tires
            if vt["vehicle_id"] == vehicle_id
        }
        positionsunica = [
            "delantera_izquierda",
            "delantera_derecha",
            "trasera_izquierda",
            "trasera_derecha",
            "repuesto",
        ]
        
        return {p: tires_s.get(p) for p in positionsunica}.get(position, "")
        


    @rx.var
    def vehicle_tires_by_position(self) -> dict[str, VehicleTire]:
        
        if not self.selected_vehicle_for_detail:
            return {}
        vehicle_id = self.selected_vehicle_for_detail[0]["id"]
        
        tires = {
            vt["position"]: vt
            for vt in self.vehicle_tires
            if vt["vehicle_id"] == vehicle_id
        }
        positions = [
            "delantera_izquierda",
            "delantera_derecha",
            "trasera_izquierda",
            "trasera_derecha",
            "repuesto",
        ]
        return {p: tires.get(p) for p in positions}

    @rx.var
    def history_for_selected_tire(self) -> list[TireHistory]:
        if not self.selected_vehicle_tire:
            return []
        history = [
            th
            for th in self.tire_history
            if th["vehicle_tire_id"] == self.selected_vehicle_tire["id"]
        ]
        return sorted(history, key=lambda x: x["fecha"], reverse=True)

    def _get_tire_info_from_id(self, tire_id: int) -> Tire | None:
        return next((t for t in self.tires if t["id"] == tire_id), None)

    @rx.event
    def get_tire_info_from_id(self, tire_id: int) -> Tire | None:
        return self._get_tire_info_from_id(tire_id)

    @rx.var
    def tire_info_by_id(self) -> dict[str, Tire]:
        return {str(t.id): t for t in self.tires}

    @rx.var
    def tire_info_for_history(self) -> Tire | None:
        if self.selected_vehicle_tire:
            return self._get_tire_info_from_id(self.selected_vehicle_tire["tire_id"])
        return None