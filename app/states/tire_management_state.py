import reflex as rx
from app.states.vehicle_state import VehicleState
from app.database.schemas import VehicleTireSchemaNuevo, HistoryTireSchemaNuevo
from app.database.db_rdtire import Vehiculo as Vehicle, VehicleTire, TireHistory, Tire
import datetime
from typing import cast, List
from pydantic import ValidationError


class TireManagementState(VehicleState):
    show_vehicle_detail_modal: bool = False
    selected_vehicle_for_detail: List[Vehicle] = []
    show_add_tire_modal: bool = False
    show_tire_history_modal: bool = False
    selected_vehicle_tire: VehicleTire | None = None
    new_vehicle_tire: VehicleTire = VehicleTire()
    tires_all_options: List[str] = []
    users_id: int = 0
    cliente_id: int = 0
    tire_id_selected: int = 0
    selected_tires_vehicle: List[Tire] = [] 
    tire_historia: list[Tire] = []
    historia_tire_veh: list[TireHistory] = []
   

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
                        "numero_tire": seleccion.numero_tire,
                        "medida_tire": seleccion.medida_tire,
                       }
                self.cliente_id=seleccion.cliente_id
                self.selected_vehicle_for_detail.append(nuevo_registro) 
            
            datos_tire_seleccion = session.exec(
                        VehicleTire.select()
                        .where(VehicleTire.vehicle_id == vehicle_id)
                    ).all()
            self.vehicle_tires=datos_tire_seleccion

            tires_data_all = session.exec(
                               Tire.select().where(
                                    Tire.cliente_id == self.cliente_id
                                )
                            ).all()
            self.selected_tires_vehicle = tires_data_all
                      #  = next(
        #     (v for v in self.vehicles if v["id"] == vehicle_id), None
        # )
        self.show_vehicle_detail_modal = True

    @rx.event
    def close_vehicle_detail(self):
        self.show_vehicle_detail_modal = False
        self.selected_vehicle_for_detail = []
        self.selected_tires_vehicle = []

    @rx.event
    def open_add_tire_to_vehicle_modal(self, vehicle_id: int, cliente_id: int, users_id: int, position: str):
        self.new_vehicle_tire={
            "id": 0,
            "vehicle_id": vehicle_id,
            "tire_id": 0 ,
            "position": position,
            "fecha_instalacion": datetime.date.today().isoformat(),
            "estado": "Nueva",
            "profundidad_actual": 8.0,
        }
        #buscar todas las tires y almacenar en variable, para seleccionar en el modal
        with rx.session() as session:
            tires_data = session.exec(
                               Tire.select().where(
                                    (Tire.cliente_id == cliente_id) & 
                                    (Tire.asignado_a_vehiculo == False)
                                )
                            ).all()
            self.tires_all_options = [f"{tire.id} - {tire.brand} {tire.model} {tire.size}" for tire in tires_data] 
            self.users_id = users_id
            self.cliente_id = cliente_id
            
            
        self.show_add_tire_modal = True

    @rx.event
    def close_add_tire_to_vehicle_modal(self):
        self.show_add_tire_modal = False
        

    @rx.event
    def handle_new_vehicle_tire_change(self, field: str, value: str):
       
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
        new_id = max([vt.id for vt in self.vehicle_tires] + [0]) + 1
        self.new_vehicle_tire["id"] = new_id
        if self.new_vehicle_tire["fecha_instalacion"] == "":
            self.new_vehicle_tire["fecha_instalacion"] = datetime.date.today().isoformat() 

        if self.new_vehicle_tire["profundidad_actual"] is None:
            return rx.window_alert("La profundidad actual no puede estar vacía.")
        if form_data is None:
            return rx.window_alert("No se recibieron datos del formulario.")

        with rx.session() as session:
            try:
                """ Validar y crear instancia de VehicleTire
                """
                vehicle_tire_instance = VehicleTireSchemaNuevo.model_validate(form_data)

                instance_tire = VehicleTire(**vehicle_tire_instance.model_dump())
                instance_tire.tire_id = self.new_vehicle_tire["tire_id"]
                instance_tire.vehicle_id = self.new_vehicle_tire["vehicle_id"]
                session.add(instance_tire)
                session.flush()  # Asegura que el ID se genere
                session.refresh(instance_tire)
                self.tire_id_selected = instance_tire.tire_id
                print(instance_tire)
                """ Crear entrada en TireHistory para la instalación de la llanta
                """
                #self.new_vehicle_tire = instance_tire
                    # self.vehicle_tires.append(self.new_vehicle_tire.copy())
                    # new_history_id = max([th["id"] for th in self.tire_history] + [0]) + 1
                history_entry: TireHistory = {
                    "id": 0,
                    "vehicletireid": instance_tire.id,
                    "cliente_id": self.cliente_id,
                    "usuario_id": self.users_id,
                    "tipo_evento": "Instalacion Inicial",
                    "fecha": instance_tire.fecha_instalacion,
                    "notas": f"Llanta nueva instalada con profundidad de {instance_tire.profundidad_actual}mm",
                    "profundidad_medida": instance_tire.profundidad_actual,
                    "odometro_lectura": instance_tire.odometro_actual,
                    "presion_tire": instance_tire.presion_tire_actual,
                }
                #self.tire_history.append(history_entry)
                history_tire_data= HistoryTireSchemaNuevo.model_validate(history_entry)
                instance_history_tire = TireHistory(**history_tire_data.model_dump())
                instance_history_tire.cliente_id = self.cliente_id
                instance_history_tire.usuario_id = self.users_id
                instance_history_tire.vehicletireid = instance_tire.id
                session.add(instance_history_tire)
                print(instance_history_tire)
                """ Actualizar estado de la llanta a 'MON' y asignado_a_vehiculo = True
                    verificar si el stock esta en cero, para crear bandera de ingreso
                """
                tire_asignado = session.exec(
                                Tire.select().where(
                                        Tire.id == self.tire_id_selected )
                                ).first()
                if tire_asignado:
                    if tire_asignado.stock == 1:
                        tire_asignado.asignado_a_vehiculo = True
                        tire_asignado.estado = "MON"
                    tire_asignado.stock = tire_asignado.stock - 1                    
                    tire_asignado.fecha_actualizacion = datetime.datetime.now()
                    session.add(tire_asignado)
                    
                    print(tire_asignado)

            except ValidationError as e:
                for err in e.errors():
                    field_name = err['loc'][0] if err['loc'] else 'general'
                    self.errors[field_name] = err['msg']
                self.has_error = True 
                return  rx.window_alert(f'error en ValidationError:  {self.errors}')                    
            except Exception as er:
                session.rollback()
                self.has_error = True
                self.errors = {
                    "general": f"se genero un error al guardar VehicleTire: {str(er)}"
                }
                return rx.window_alert(self.errors)      
            except field as e:
                session.rollback()
                self.has_error = True
                self.errors = {
                    field: f"Error en el campo {field}: {str(e)}"
                }
                return rx.window_alert(self.errors)
            except TypeError as te:
                session.rollback()
                self.has_error = True
                self.errors = {
                    "general": f"TypeError al guardar VehicleTire: {str(te)}"
                }
                return rx.window_alert(self.errors)
            except ValueError as ve:
                session.rollback()
                self.has_error = True
                self.errors = {
                    "general": f"ValueError al guardar VehicleTire: {str(ve)}"
                }
                return rx.window_alert(self.errors)
            except object as oe:
                session.rollback()
                self.has_error = True
                self.errors = {
                    "general": f"Object error al guardar VehicleTire: {str(oe)}"
                }
                return rx.window_alert(self.errors)
            else:
                session.commit()
                # Actualizar la lista local de vehicle_tires y tire_history
                self.new_vehicle_tire = instance_tire.model_dump()
                rx.window_alert("Llanta agregada al vehículo correctamente.")
            
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
            (vt for vt in self.vehicle_tires if vt.id == vehicle_tire_id), None
        )
        
        """ busco la tire seleccionada y caracteristicas"""
        with rx.session() as session:
            detalle_tire = session.exec(Tire.select().where(
                Tire.id == self.selected_vehicle_tire.tire_id
            )).all()

            self.tire_historia = detalle_tire

            detalle_tire_his = session.exec(TireHistory.select().where(
                TireHistory.vehicletireid == vehicle_tire_id
            )).all()

            self.historia_tire_veh = detalle_tire_his 
        self.show_tire_history_modal = True

    @rx.event
    def close_tire_history_modal(self):
        self.show_tire_history_modal = False
        self.selected_vehicle_tire = None
        self.tire_historia = []
        self.historia_tire_veh = []

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
    def vehicle_tires_by_position(self) -> dict[str, VehicleTire | None]:
        
        if not self.selected_vehicle_for_detail:
            return {}
        vehicle_id = self.selected_vehicle_for_detail[0]["id"]
       
        tires = {
            vt.position: vt
            for vt in self.vehicle_tires
            if vt.vehicle_id == vehicle_id
        }
        if self.selected_vehicle_for_detail[0]["numero_tire"] == 4:
            positions = [
                "delantera_izquierda",
                "delantera_derecha",
                "trasera_izquierda",
                "trasera_derecha",
                "repuesto",
            ]
        else:
            positions = [
                "delantera_izquierda",
                "delantera_derecha",
                "trasera_izquierda_ext",
                "trasera_izquierda_int",
                "trasera_derecha_ext",
                "trasera_derecha_int",
                "repuesto",
            ]
        #print( {p: tires.get(p) for p in positions})
        return {p: tires.get(p) for p in positions}

    @rx.var
    def history_for_selected_tire(self) -> list[TireHistory]:
        if not self.selected_vehicle_tire:
            return []
        history = [
            th for th in self.historia_tire_veh
        ]
        return sorted(history, key=lambda x: x.fecha, reverse=True)

    def _get_tire_info_from_id(self, tire_id: int) -> Tire | None:
        return next((t for t in self.tire_historia if t["id"] == tire_id), None)

    @rx.event
    def get_tire_info_from_id(self, tire_id: int) -> Tire | None:
        return self._get_tire_info_from_id(tire_id)

    # @rx.var
    # def tire_info_by_id(self) -> dict[str, Tire]:
    #     print({str(t.id): t for t in self.tires})
    #     return {str(t.id): t for t in self.tires}

    @rx.var
    def tire_info_by_id(self) -> dict[int, Tire | None]:
        if not self.selected_tires_vehicle:
            return {}
        #print({t.id: t for t in self.selected_tires_vehicle})
        #print(self._get_tire_info_from_id(self.self.selected_tires_vehicle["id"]))
        return {t.id: t for t in self.selected_tires_vehicle}

    @rx.var
    def tire_info_for_history(self) -> Tire | None:
        if self.selected_vehicle_tire:
            #return self._get_tire_info_from_id(self.selected_vehicle_tire["tire_id"])

            return next((t for t in self.tire_historia), None)

        return None