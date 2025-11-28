import reflex as rx 
from app.states.base_state import BaseState
from typing import TypedDict
import logging
import datetime
from app.database.db_rdtire import Usuario,Vehiculo as Vehicle, Cliente, TireHistory, Tire, VehicleTire
from app.database.schemas import TireSchemaNuevo
from pydantic import ValidationError

class TiresState(BaseState):

    @rx.event
    def open_add_product_modal(self, cliente_id: int):
        self.show_add_product_modal = True
        #self.new_product = Tire() 
        self.tire_cliente_id = cliente_id
        self.new_product = {
                        "id":0,
                        "brand": "",
                        "size": "",
                        "dot": "",
                        "model": "",
                        "type": "RADIAL",
                        "season":"",
                        "speed_rating":"",
                        "load_index": 0,
                        "price": 0,
                        "stock": 0,
                        "image_url": "",
                       }

    @rx.event
    def close_add_product_modal(self):
        self.show_add_product_modal = False
        self.tire_cliente_id = 0

    @rx.event
    def open_product_detail_modal(self, tire: Tire):
        self.selected_tire = tire
        self.show_product_detail_modal = True

    @rx.event
    def close_product_detail_modal(self):
        self.show_product_detail_modal = False
        self.selected_tire = None

    @rx.event
    def handle_new_product_change(self, field: str, value: str):
         if field == "price" or field == "stock" or field == "id":
             try:
                 self.new_product[field] = (
                     int(value) if field != "price" else float(value)
                 )
             except (ValueError, TypeError) as e:
                 logging.exception(f"Error converting value for field {field}: {e}")
         else:
             self.new_product[field] = value
       

    @rx.event
    def mostrar_tires(self, cliente_id: int):
        #self.mostrar_usuario_tabla = True
        with rx.session() as session:
            self.tires= session.exec(
                               Tire.select().where(
                                    cliente_id == cliente_id
                                )
                            ).all()
    

    @rx.event
    def save_new_product(self, form_data: dict):
        if form_data is None:
            return
        self.form_datap = form_data
        self.stock_original = self.form_datap['stock']
        if int(self.stock_original) > 4:
            return rx.window_alert("El numero maximo de stock es 4, Inventario Individual crea un registro por llanta")
        with rx.session() as session:
            try:
                #print(form_data)
                instance_data = TireSchemaNuevo.model_validate(form_data)
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
            
            instance = Tire(**instance_data.model_dump())
            #instance.creado_por = self.vehicle_creado_por
            instance.cliente_id = self.tire_cliente_id
            instance.stock = 1
                #print(instance)
            try:    
                lista_de_datos = []    
                for i in range(int(self.stock_original)):
                    lista_de_datos.append(instance)

                nuevos_datos_db = []
                for datos in lista_de_datos:
                    nuevos_datos=Tire(
                        brand = datos.brand,
                        size = datos.size,
                        dot = datos.dot,
                        model = datos.model,
                        type = datos.type,
                        season= datos.season,
                        speed_rating = datos.speed_rating,
                        load_index = datos.load_index,
                        price = datos.price,
                        stock = datos.stock,
                        asignado_a_vehiculo = datos.asignado_a_vehiculo,
                        estado = datos.estado,
                        image_url = datos.image_url,
                        cliente_id = datos.cliente_id,
                    )
                    nuevos_datos_db.append(nuevos_datos)
                print(nuevos_datos_db)
                session.add_all(nuevos_datos_db)    
                session.commit()
            except Exception as e:
                session.rollback()
                print(f"❌ Error al guardar las llantas. Transacción revertida: {e}")
                return rx.window_alert(f"❌ Error al guardar las llantas. Transacción revertida: {e}")
            #session.refresh(instance)
            
        self.show_add_product_modal = False 
        return  rx.window_alert("¡Registros guardados con éxito!")  

    @rx.event
    def add_product(self):
        new_id = max([t["id"] for t in self.tires]) + 1 if self.tires else 1
        self.new_product["id"] = new_id
        if not self.new_product["image_url"]:
            self.new_product["image_url"] = "/placeholder.svg"
        self.tires.append(self.new_product)
        self._reset_new_product_form()
        self.show_add_product_modal = False

    def _reset_new_product_form(self):
        self.new_product = {
            "id": 0,
            "brand": "",
            "model": "",
            "size": "",
            "type": "",
            "season": "",
            "speed_rating": "",
            "load_index": "",
            "price": 0.0,
            "stock": 0,
            "image_url": "",
            "inventory_history": [],
        }

    @rx.var
    def filtered_tires(self) -> list[Tire]:
        query = self.search_query.lower()
        tires = self.tires
        if query:
            tires = [
                t
                for t in self.tires
                if query in t["brand"].lower()
                or query in t["model"].lower()
                or query in t["size"].lower()
            ]
        if self.filter_brand:
            tires = [t for t in tires if t["brand"] == self.filter_brand]
        if self.filter_size:
            tires = [t for t in tires if t["size"] == self.filter_size]
        if self.filter_type:
            tires = [t for t in tires if t["type"] == self.filter_type]
        if self.filter_season:
            tires = [t for t in tires if t["season"] == self.filter_season]
        if self.min_price:
            try:
                min_p = float(self.min_price)
                tires = [t for t in tires if t["price"] >= min_p]
            except ValueError as e:
                logging.exception(f"Error converting min_price: {e}")
        if self.max_price:
            try:
                max_p = float(self.max_price)
                tires = [t for t in tires if t["price"] <= max_p]
            except ValueError as e:
                logging.exception(f"Error converting max_price: {e}")
        return tires

    @rx.var
    def unique_brands(self) -> list[str]:
        return sorted(list(set((t.brand for t in self.tires))))

    @rx.var
    def unique_sizes(self) -> list[str]:
        return sorted(list(set((t.size for t in self.tires))))

    @rx.var
    def unique_types(self) -> list[str]:
        return sorted(list(set((t.type for t in self.tires))))

    @rx.var
    def unique_seasons(self) -> list[str]:
        return sorted(list(set((t.season for t in self.tires))))
    
