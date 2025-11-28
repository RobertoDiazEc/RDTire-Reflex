import reflex as rx
from typing import TypedDict
import logging
import datetime
from app.database.db_rdtire import Usuario,Vehiculo as Vehicle, Cliente, TireHistory, Tire, VehicleTire
from app.database.schemas import TireSchemaNuevo
from pydantic import ValidationError


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



CUSTOMER_DATA: list[Customer] = [
    {
        "id": 1,
        "name": "John Smith",
        "email": "john@example.com",
        "phone": "123-456-7890",
    },
    {"id": 2, "name": "Jane Doe", "email": "jane@example.com", "phone": "098-765-4321"},
]

class BaseState(rx.State):
    form_datap: dict = {}
    tires: list[Tire] = []
    customers: list[Customer] = []
    usuarios:list[Usuario] = []
    vehicles: list[Vehicle] = []
    vehicle_tires: list[VehicleTire] = []
    tire_history: list[TireHistory] = []
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
    new_product: Tire = Tire()
    tire_cliente_id: int = 0
    cliente_id_global: int = 0
    stock_original: str = ""
    @rx.event
    def toggle_sidebar(self):
        self.sidebar_open = not self.sidebar_open

    