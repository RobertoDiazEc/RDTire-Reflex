import reflex as rx
from typing import List, Optional
from datetime import datetime
from app.states.base_state import BaseState
from app.database.db_rdtire import VehicleTire, TireHistory, Tire  # ajusta el import según tu proyecto


class MultiTireInspectionState(BaseState):
    # Contexto
    vehiculo_id: Optional[int] = None
    cliente_id: Optional[int] = None
    usuario_id: Optional[int] = None

    # Lista de llantas a inspeccionar
    # Cada item será un dict:
    # {
    #   "vehicletireid": int,
    #   "position": str,
    #   "profundidad_medida": float,
    #   "presion_tire": int,
    #   "odometro_lectura": int,
    #   "notas": str,
    #   "estado_visual_checks": List[str],
    # }
    llantas: List[VehicleTire] = []

    # --------- Cargar llantas del vehículo ---------

    def load_llantas(self, vehiculo_id: int, cliente_id: int, usuario_id: int):
        """Cargar las llantas (VehicleTire) montadas en un vehículo."""
        self.vehiculo_id = vehiculo_id
        self.cliente_id = cliente_id
        self.usuario_id = usuario_id

        with rx.session() as session:
            vts = (
                session.query(VehicleTire)
                .filter(VehicleTire.vehicle_id == vehiculo_id)
                .all()
            )

            self.llantas = [
                {
                    "vehicletireid": vt.id,  # id autogenerado por rx.Model
                    "position": vt.position,
                    "profundidad_medida": vt.profundidad_actual or 0.0,
                    "presion_tire": vt.presion_tire_actual or 0,
                    "odometro_lectura": vt.odometro_actual or 0,
                    "notas": "",
                    "estado_visual_checks": [],  # se llena desde los checkbox
                }
                for vt in vts
            ]

    # --------- Actualizar campos por índice ---------

    def update_profundidad(self, index: int, value: str):
        try:
            self.llantas[index]["profundidad_medida"] = float(value) if value else 0.0
        except ValueError:
            self.llantas[index]["profundidad_medida"] = 0.0

    def update_presion(self, index: int, value: str):
        try:
            self.llantas[index]["presion_tire"] = int(value) if value else 0
        except ValueError:
            self.llantas[index]["presion_tire"] = 0

    def update_odometro(self, index: int, value: str):
        try:
            self.llantas[index]["odometro_lectura"] = int(value) if value else 0
        except ValueError:
            self.llantas[index]["odometro_lectura"] = 0

    def update_notas(self, index: int, value: str):
        self.llantas[index]["notas"] = value

    def update_estado_visual_checks(self, index: int, values: List[str]):
        self.llantas[index]["estado_visual_checks"] = values

    # --------- Lógica de criticidad por llanta ---------

    def _calcular_criticidad_llanta(self, llanta: dict) -> str:
        """
        Reglas ejemplo:
        - profundidad < 3 mm => CRITICA
        - 'Cortes / grietas' => CRITICA
        - 'Bultos' o 'Desgaste irregular' => OBS
        - resto => OK
        """
        checks = set(llanta["estado_visual_checks"])
        profundidad = llanta["profundidad_medida"]

        if profundidad < 3:
            return "CRITICA"
        if "Cortes / grietas" in checks:
            return "CRITICA"
        if "Bultos" in checks or "Desgaste irregular" in checks:
            return "OBS"
        return "OK"

    # --------- Guardar inspecciones para todas las llantas ---------

    def guardar_inspecciones(self):
        if self.cliente_id is None or self.usuario_id is None:
            return

        if not self.llantas:
            return

        with rx.session() as session:
            registros = []

            for ll in self.llantas:
                criticidad = self._calcular_criticidad_llanta(ll)
                estado_visual_str = (
                    ";".join(ll["estado_visual_checks"])
                    if ll["estado_visual_checks"]
                    else None
                )

                history = TireHistory(
                    vehicletireid=ll["vehicletireid"],
                    tipo_evento="INSPECCION",
                    notas=ll["notas"],
                    profundidad_medida=ll["profundidad_medida"],
                    odometro_lectura=ll["odometro_lectura"],
                    presion_tire=ll["presion_tire"],
                    estado_visual=estado_visual_str,
                    criticidad=criticidad,
                    realizador=str(self.usuario_id),
                    cliente_id=self.cliente_id,
                    usuario_id=self.usuario_id,
                )
                registros.append(history)

            session.add_all(registros)
            session.commit()

        # Opcional: limpiar notas y checks, pero mantener lecturas si quieres
        for ll in self.llantas:
            ll["notas"] = ""
            ll["estado_visual_checks"] = []