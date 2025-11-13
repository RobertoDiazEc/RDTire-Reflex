import reflex as rx
from app.states.base_state import BaseState
from app.states.auth_state import AuthState
import datetime
import logging
from typing import cast
from app.database.db_rdtire import Vehiculo as Vehicle
from app.database.schemas import VehiculoSchemaNuevo
from typing import List
from pydantic import ValidationError



class VehicleState(BaseState):
    form_data: dict = {}
    errors: dict = {}
    has_error: bool = False
    show_vehicle_modal: bool = False
    is_editing_vehicle: bool = False
    selected_vehicle: Vehicle | None = None
    new_vehicle: Vehicle = Vehicle()
    vehicle_creado_por: str = ""
    vehicle_cliente_id: int = 0 
    

    @rx.event
    def open_add_vehicle_modal(self, creado_por: str, cliente_id: int):
        self.is_editing_vehicle = False
        self.new_vehicle = Vehicle()
        self.show_vehicle_modal = True
        self.vehicle_creado_por = creado_por
        self.vehicle_cliente_id = cliente_id

    @rx.event
    def open_edit_vehicle_modal(self, vehicle: Vehicle):
        self.is_editing_vehicle = True
        self.selected_vehicle = vehicle
        self.new_vehicle = vehicle
        self.show_vehicle_modal = True

    @rx.event
    def close_vehicle_modal(self):
        self.show_vehicle_modal = False
        self.selected_vehicle = None
        self.is_editing_vehicle = False

    @rx.event
    def handle_vehicle_change(self, field: str, value: str):
        pass
        
    @rx.event
    def mostrar_vehiculos(self, cliente_id: int):
        #self.mostrar_usuario_tabla = True
        with rx.session() as session:
            self.vehicles= session.exec(
                               Vehicle.select().where(
                                    cliente_id == cliente_id
                                )
                            ).all()
            
    @rx.event
    def save_vehicle(self, form_data: dict):
        self.form_data = form_data
        with rx.session() as session:
            if self.is_editing_vehicle and self.selected_vehicle:
                try:
                    #print(self.form_data)
                    instance_data = VehiculoSchemaNuevo.model_validate(form_data)
                except ValidationError as e:
                    for err in e.errors():
                        field_name = err['loc'][0] if err['loc'] else 'general'
                        self.errors[field_name] = err['msg']
                    self.has_error = True 
                    return  rx.window_alert(self.errors)  
                except Exception as er:
                    self.has_error = True
                    self.errors = {
                        "general": f"se genero un error al editar: {str(er)}"
                    }
                    return rx.window_alert(self.errors())
                vehicle_actual=session.exec(
                    Vehicle.select()
                    .where(Vehicle.id == self.new_vehicle.id)
                    ).first()
                vehicle_actual.placa = instance_data.placa
                vehicle_actual.marca = instance_data.marca
                vehicle_actual.modelo = instance_data.modelo
                vehicle_actual.anio = instance_data.anio
                vehicle_actual.tipo = instance_data.tipo    
                
                
                #print(instance)
                session.add(vehicle_actual)

                session.commit()
                session.refresh(vehicle_actual)

            else:
                try:
                    #print(self.form_data)
                    
                    instance_data = VehiculoSchemaNuevo.model_validate(form_data)
                except ValidationError as e:
                    for err in e.errors():
                        field_name = err['loc'][0] if err['loc'] else 'general'
                        self.errors[field_name] = err['msg']
                    self.has_error = True 
                    return  rx.window_alert(self.errors)  
                except Exception as er:
                    self.has_error = True
                    self.errors = {
                        "general": f"se genero un error al Crear : {str(er)}"
                    }
                    return rx.window_alert(self.errors())
                
                instance = Vehicle(**instance_data.model_dump())
                instance.creado_por = self.vehicle_creado_por
                instance.cliente_id = self.vehicle_cliente_id
                #print(instance)
                session.add(instance)

                session.commit()

                session.refresh(instance)
        self.close_vehicle_modal()

    @rx.event
    def delete_vehicle(self, vehicle_id: int):
        self.vehicles = [v for v in self.vehicles if v["id"] != vehicle_id]
        self.vehicle_tires = [
            vt for vt in self.vehicle_tires if vt["vehicle_id"] != vehicle_id
        ]