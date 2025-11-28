import reflex as rx
from app.states.tire_management_state import TireManagementState
from app.states.base_state import Vehicle, VehicleTire, TireHistory, Tire
from datetime import datetime, timezone



class InspectionState(TireManagementState):
    show_inspection_modal: bool = False
    selected_vehicle_for_inspection: Vehicle | None = None
    current_inspection_tires: list[VehicleTire] = []
    current_inspection_tires_detall: list[Tire] = []
    inspection_depths: dict[int, str] = {}
    tire_vehiculo_brand: dict[int, str] = {}
    tire_vehiculo_size: dict[int, str] = {}
    inspection_notes: str = ""
    inspection_odometro: int = 0
    tires_vehicle: list[Tire] = []
    date_now: datetime = datetime.now(timezone.utc)
    selected_estado: list = []
    llantas: list[dict[str, None]] = []
    inspeccion_valor: str = "Inspección"
    mesaje_error_pantalla: list = []
    rotar_posicion_llanta: list = []
    rotacion_item: str = ""

    @rx.event
    def set_rotacion_item(self, item: str):
        if item=="Radial":
            self.rotacion_item = "Rotacion en X (LF -> RR) (RF -> LR) (LR -> LF) (RR -> RF)"
        else: 
            self.rotacion_item = "Rotacion en || (LF -> LR) (RF -> RR) (LR -> LF) (RR -> RF)"   
        self.change_posicion_valor(item)

    @rx.event
    def change_inspeccion_valor(self, inspeccion_valor: str):
        """Change the select value var."""
        self.inspeccion_valor = inspeccion_valor

    def set_selected_estado(self, value: list):
        self.selected_estado = value

    @rx.event
    def estado_visual_checked(self, indicador: int, opcion: str, checked: bool):
        
        checks= set(self.llantas[indicador]["estado_visual_checks"])
        if checked:
            checks.add(opcion)
        else:
            checks.discard(opcion)
        self.llantas[indicador]["estado_visual_checks"] = list(checks)
        print(self.llantas)       

    @rx.event
    def open_inspection_modal(self, vehicle: Vehicle):
        self.selected_vehicle_for_inspection = vehicle
        """buscar los Tires del vehiculo
        """
        with rx.session() as session:
            "buscar todas las Tires de cada vehiculo montado"
            tires_asignadas = session.exec(VehicleTire.select().where(
                VehicleTire.vehicle_id == vehicle.id
                )).all()
            
            self.current_inspection_tires = tires_asignadas
            self.llantas = [
                {
                    "tire_id": vt.tire_id,
                    "vehicletireid": vt.id,
                    "tipo_evento": self.inspeccion_valor,
                    "notas": "",
                    "profundidad_medida": vt.profundidad_actual, 
                    "odometro_lectura": vt.odometro_actual,
                    "presion_tire": 0, 
                    "realizador": "",
                    "criticidad": "OK",
                    "posicion_anterior": "",
                    "posicion_nueva": "",
                    "motivo_baja": "",
                    "tipo_reparacion":"",
                    "costo_reparacion": 0,
                    "cliente_id": 0,
                    "usuario_id": 0,    
                    # AQUÍ: lista independiente por llanta
                    "estado_visual_checks": [],    # <- se llena desde los checkboxes
                }
                for vt in tires_asignadas
            ]
            self.mesaje_error_pantalla= ["" for vt in tires_asignadas]
            self.rotar_posicion_llanta= ["" for vt in range(4)]
            """Buscar las caracteristicas de la Tire"""
            tires_data_all = session.exec(
                               Tire.select().where(
                                    Tire.cliente_id == self.cliente_id_global
                                )
                            ).all()
            self.current_inspection_tires_detall = tires_data_all
           
        self.inspection_depths = {
            vt.id: str(vt.profundidad_actual) for vt in self.current_inspection_tires
        }

        self.tire_vehiculo_brand ={
            t.id: t.brand for t in self.current_inspection_tires_detall
        }

        self.tire_vehiculo_size ={
            t.id: t.size for t in self.current_inspection_tires_detall
        } 
        # self.estado_llanta = {
        #     t.id: t.position for t in self.current_inspection_tires
        # }
        self.inspection_notes = ""
        self.show_inspection_modal = True

    @rx.event
    def close_inspection_modal(self):
        self.show_inspection_modal = False
        self.selected_vehicle_for_inspection = None
        self.current_inspection_tires = []
        self.current_inspection_tires_detall = []
        self.inspection_depths = {}
        self.tire_vehiculo_size = {}
        self.tire_vehiculo_brand = {}
        self.llantas = []
        self.inspection_notes = ""
        self.mesaje_error_pantalla=[]
        self.inspection_odometro= 0

    @rx.event
    def handle_presion_change(self, vehicle_tire_id: int, depth: str):
        self.llantas[vehicle_tire_id] =float(depth) 
    
    @rx.event
    def handle_depth_change(self, vehicle_tire_id: int, depth: str, indicador: int):
       
        dep_anterior= self.inspection_depths.get(vehicle_tire_id , "")
        
        if float(depth) <= float(dep_anterior): 
            #self.inspection_depths[vehicle_tire_id] = depth
            self.llantas[indicador]["profundidad_medida"] = float(depth) if depth else 0.0
            self.mesaje_error_pantalla[indicador]=""
        else:
            self.mesaje_error_pantalla[indicador]= f"Profundidad no mayor a {dep_anterior}"

    @rx.event
    def change_posicion_valor(self, item: str):
        if item == "Radial":
            self.rotar_posicion_llanta[0]="Tracera Derecha"
            self.rotar_posicion_llanta[1]="Tracera Izquierda"
            self.rotar_posicion_llanta[2]="Delantera Izquierda"
            self.rotar_posicion_llanta[3]="Delantera Derecha"
        else:
            self.rotar_posicion_llanta[0]="Tracera Izquierda"
            self.rotar_posicion_llanta[1]="Tracera Derecha"
            self.rotar_posicion_llanta[2]="Delantera Izquierda"
            self.rotar_posicion_llanta[3]="Delantera Derecha" 
        self.inspection_notes=f"cambios realizados: {self.rotacion_item}"

    @rx.event
    def save_inspection(self):
        if not self.selected_vehicle_for_inspection:
            return rx.window_alert("Sin datos para Inspeccionar")
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
                if new_depth <= 1.6:
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

    @rx.var
    def inspection_tires_by_position(self) -> dict[str, VehicleTire | None]:
        if not self.current_inspection_tires:
            return {}
       
        tires = {
            vt.position: vt
            for vt in self.current_inspection_tires
        }
        positions = [
                "delantera_izquierda",
                "delantera_derecha",
                "trasera_izquierda",
                "trasera_derecha",
            ]
        # else:
        #     positions = [
        #         "delantera_izquierda",
        #         "delantera_derecha",
        #         "trasera_izquierda_ext",
        #         "trasera_izquierda_int",
        #         "trasera_derecha_ext",
        #         "trasera_derecha_int",
        #         "repuesto",
        #     ]
        #print( {p: tires.get(p) for p in positions})
        return {p: tires.get(p) for p in positions}  

    @rx.var
    def inspect_tire_info_by_id(self) -> dict[int, VehicleTire]:
        if not self.current_inspection_tires:
            return {}
        #print({t.id: t for t in self.current_inspection_tires})
        #print(self._get_tire_info_from_id(self.self.selected_tires_vehicle["id"]))
        return {t.id: t for t in self.current_inspection_tires} 