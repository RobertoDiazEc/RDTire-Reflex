import reflex as rx 

from app.states.multinspect_state import MultiTireInspectionState
from app.states.vehicle_state import VehicleState
from app.states.base_state import Vehicle, VehicleTire

# def tarjeta_llanta_multi(llanta: VehicleTire) -> rx.Component:
#     return rx.card(
#         rx.text(f"Posición: {llanta['position']}", weight="bold"),

#         rx.hstack(
#             rx.text("Profundidad (mm):"),
#             rx.input(
#                 type="number",
#                 value=str(llanta["profundidad_medida"]),
#                 width="80px",
#                 on_change=lambda v, i=index: MultiTireInspectionState.update_profundidad(i, v),
#             ),
#         ),

#         rx.hstack(
#             rx.text("Presión (psi):"),
#             rx.input(
#                 type="number",
#                 value=str(llanta["presion_tire"]),
#                 width="80px",
#                 on_change=lambda v, i=index: MultiTireInspectionState.update_presion(i, v),
#             ),
#         ),

#         rx.hstack(
#             rx.text("Odómetro (km):"),
#             rx.input(
#                 type="number",
#                 value=str(llanta["odometro_lectura"]),
#                 width="100px",
#                 on_change=lambda v, i=index: MultiTireInspectionState.update_odometro(i, v),
#             ),
#         ),

#         rx.text("Estado visual:"),
#         rx.vstack(
#             rx.checkbox(
#                 "Cortes / grietas",
#                 is_checked="Cortes / grietas" in llanta["estado_visual_checks"],
#                 on_change=lambda checked, i=index: MultiTireInspectionState.toggle_estado_visual(
#                     i, "Cortes / grietas", checked
#                 ),
#             ),
#             rx.checkbox(
#                 "Bultos",
#                 is_checked="Bultos" in llanta["estado_visual_checks"],
#                 on_change=lambda checked, i=index: MultiTireInspectionState.toggle_estado_visual(
#                     i, "Bultos", checked
#                 ),
#             ),
#             rx.checkbox(
#                 "Desgaste irregular",
#                 is_checked="Desgaste irregular" in llanta["estado_visual_checks"],
#                 on_change=lambda checked, i=index: MultiTireInspectionState.toggle_estado_visual(
#                     i, "Desgaste irregular", checked
#                 ),
#             ),
#             rx.checkbox(
#                 "Objeto incrustado",
#                 is_checked="Objeto incrustado" in llanta["estado_visual_checks"],
#                 on_change=lambda checked, i=index: MultiTireInspectionState.toggle_estado_visual(
#                     i, "Objeto incrustado", checked
#                 ),
#             ),
#             align_items="flex-start",
#             spacing="1",
#         ),

#         rx.text("Notas:"),
#         rx.text_area(
#             value=llanta["notas"],
#             on_change=lambda v, i=index: MultiTireInspectionState.update_notas(i, v),
#         ),

#         spacing="3",
#         padding="1em",
#         width="100%",
#     )


def inspeccion_vehiculo_ui() ->rx.Component:
    return rx.container(
        rx.heading("Inspección de llantas del vehículo"),

        # rx.grid(
        #     rx.foreach(
        #         MultiTireInspectionState.llantas,
        #         lambda llanta, i: tarjeta_llanta_multi(llanta, i),
        #     ),
        #     columns=[1, 2, 3],  # móvil / tablet / desktop
        #     spacing="4",
        # ),

        rx.button(
            "Guardar inspecciones",
            on_click=MultiTireInspectionState.guardar_inspecciones,
            margin_top="1em",
            color_scheme="green",
        ),

        padding="2em",
    )