import reflex as rx
from typing import TypedDict
import logging
import datetime


class InventoryAdjustment(TypedDict):
    timestamp: str
    reason: str
    amount: int


class Customer(TypedDict):
    id: int
    name: str
    email: str
    phone: str


class SaleItem(TypedDict):
    tire_id: int
    quantity: int
    price_at_sale: float


class Sale(TypedDict):
    id: int
    timestamp: str
    customer_id: int
    items: list[SaleItem]
    total: float
    payment_method: str


class Vehicle(TypedDict):
    id: int
    placa: str
    marca: str
    modelo: str
    ano: int
    tipo: str
    fecha_registro: str


class VehicleTire(TypedDict):
    id: int
    vehicle_id: int
    tire_id: int
    position: str
    fecha_instalacion: str
    estado: str
    profundidad_actual: float


class TireHistory(TypedDict):
    id: int
    vehicle_tire_id: int
    tipo_evento: str
    fecha: str
    notas: str
    profundidad_medida: float | None


class Tire(TypedDict):
    id: int
    brand: str
    model: str
    size: str
    type: str
    season: str
    speed_rating: str
    load_index: str
    price: float
    stock: int
    image_url: str
    inventory_history: list[InventoryAdjustment]


TIRE_DATA: list[Tire] = [
    {
        "id": 1,
        "brand": "Michelin",
        "model": "Pilot Sport 4S",
        "size": "255/35R19",
        "type": "Performance",
        "season": "Summer",
        "speed_rating": "Y",
        "load_index": "96",
        "price": 350.0,
        "stock": 50,
        "image_url": "/placeholder.svg",
        "inventory_history": [],
    },
    {
        "id": 2,
        "brand": "Bridgestone",
        "model": "Blizzak WS90",
        "size": "225/45R17",
        "type": "Winter",
        "season": "Winter",
        "speed_rating": "H",
        "load_index": "91",
        "price": 180.0,
        "stock": 8,
        "image_url": "/placeholder.svg",
        "inventory_history": [],
    },
    {
        "id": 3,
        "brand": "Goodyear",
        "model": "Assurance WeatherReady",
        "size": "235/60R18",
        "type": "All-Season",
        "season": "All-Season",
        "speed_rating": "V",
        "load_index": "103",
        "price": 210.0,
        "stock": 45,
        "image_url": "/placeholder.svg",
        "inventory_history": [],
    },
    {
        "id": 4,
        "brand": "Continental",
        "model": "ExtremeContact DWS06",
        "size": "245/40R18",
        "type": "All-Season",
        "season": "All-Season",
        "speed_rating": "Y",
        "load_index": "97",
        "price": 230.0,
        "stock": 60,
        "image_url": "/placeholder.svg",
        "inventory_history": [],
    },
    {
        "id": 5,
        "brand": "Pirelli",
        "model": "P Zero",
        "size": "275/30R20",
        "type": "Performance",
        "season": "Summer",
        "speed_rating": "Y",
        "load_index": "97",
        "price": 420.0,
        "stock": 5,
        "image_url": "/placeholder.svg",
        "inventory_history": [],
    },
    {
        "id": 6,
        "brand": "Michelin",
        "model": "CrossClimate2",
        "size": "215/55R17",
        "type": "All-Season",
        "season": "All-Season",
        "speed_rating": "V",
        "load_index": "94",
        "price": 250.0,
        "stock": 70,
        "image_url": "/placeholder.svg",
        "inventory_history": [],
    },
]
CUSTOMER_DATA: list[Customer] = [
    {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "123-456-7890",
    },
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com", "phone": "098-765-4321"},
]
VEHICLE_DATA: list[Vehicle] = [
    {
        "id": 1,
        "placa": "PCJ-1234",
        "marca": "Toyota",
        "modelo": "Hilux",
        "ano": 2022,
        "tipo": "Camioneta",
        "fecha_registro": "2023-01-15",
    },
    {
        "id": 2,
        "placa": "GKL-5678",
        "marca": "Ford",
        "modelo": "Ranger",
        "ano": 2021,
        "tipo": "Camioneta",
        "fecha_registro": "2022-11-20",
    },
]
VEHICLE_TIRE_DATA: list[VehicleTire] = [
    {
        "id": 1,
        "vehicle_id": 1,
        "tire_id": 1,
        "position": "delantera_izquierda",
        "fecha_instalacion": "2023-05-10",
        "estado": "En uso",
        "profundidad_actual": 6.5,
    },
    {
        "id": 2,
        "vehicle_id": 1,
        "tire_id": 4,
        "position": "delantera_derecha",
        "fecha_instalacion": "2023-05-10",
        "estado": "En uso",
        "profundidad_actual": 6.8,
    },
    {
        "id": 3,
        "vehicle_id": 2,
        "tire_id": 6,
        "position": "delantera_izquierda",
        "fecha_instalacion": "2023-08-20",
        "estado": "Advertencia",
        "profundidad_actual": 2.5,
    },
]
TIRE_HISTORY_DATA: list[TireHistory] = [
    {
        "id": 1,
        "vehicle_tire_id": 1,
        "tipo_evento": "Instalacion",
        "fecha": "2023-05-10",
        "notas": "Llanta nueva instalada",
        "profundidad_medida": 8.0,
    },
    {
        "id": 2,
        "vehicle_tire_id": 1,
        "tipo_evento": "Inspeccion",
        "fecha": "2023-09-15",
        "notas": "Chequeo de rutina",
        "profundidad_medida": 6.5,
    },
    {
        "id": 3,
        "vehicle_tire_id": 3,
        "tipo_evento": "Instalacion",
        "fecha": "2023-08-20",
        "notas": "Llanta nueva instalada",
        "profundidad_medida": 8.0,
    },
    {
        "id": 4,
        "vehicle_tire_id": 3,
        "tipo_evento": "Inspeccion",
        "fecha": "2023-11-30",
        "notas": "Desgaste notable",
        "profundidad_medida": 2.5,
    },
]


class BaseState(rx.State):
    tires: list[Tire] = TIRE_DATA
    customers: list[Customer] = CUSTOMER_DATA
    vehicles: list[Vehicle] = VEHICLE_DATA
    vehicle_tires: list[VehicleTire] = VEHICLE_TIRE_DATA
    tire_history: list[TireHistory] = TIRE_HISTORY_DATA
    sidebar_open: bool = True
    search_query: str = ""
    filter_brand: str = ""
    filter_size: str = ""
    filter_type: str = ""
    filter_season: str = ""
    min_price: str = ""
    max_price: str = ""
    show_add_product_modal: bool = False
    show_product_detail_modal: bool = False
    selected_tire: Tire | None = None
    new_product: Tire = {
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

    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    @rx.event
    def open_add_product_modal(self):
        self.show_add_product_modal = True

    @rx.event
    def close_add_product_modal(self):
        self.show_add_product_modal = False

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
        return sorted(list(set((t["brand"] for t in self.tires))))

    @rx.var
    def unique_sizes(self) -> list[str]:
        return sorted(list(set((t["size"] for t in self.tires))))

    @rx.var
    def unique_types(self) -> list[str]:
        return sorted(list(set((t["type"] for t in self.tires))))

    @rx.var
    def unique_seasons(self) -> list[str]:
        return sorted(list(set((t["season"] for t in self.tires))))