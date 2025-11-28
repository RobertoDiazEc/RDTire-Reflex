import reflex as rx 
from app.states.inspections_state import InspectionState
from app.states.base_state import Vehicle, VehicleTire


"""pantalla de INSPECCION - 
    con opciones de estado visual"""
def tire_inspection_row(vehicle_tire: VehicleTire, indicador: int) -> rx.Component:
        
        return rx.el.div(
            rx.el.div(
                rx.el.p(
                    vehicle_tire["position"].replace("_", " ").title(),
                    class_name="font-semibold",
                ),
                rx.el.p(
                    f"{InspectionState.tire_vehiculo_brand.get(vehicle_tire['tire_id'], "")} {InspectionState.tire_vehiculo_size.get(vehicle_tire['tire_id'], "")}",
                    class_name="text-sm text-gray-600",
                ),
                
                rx.text("Presión(psi):"),
                rx.input(
                    type="number",
                    on_blur=lambda val: InspectionState.handle_presion_change(
                        vehicle_tire["id"], val
                    ),
                    width="100px",
                ),
              
                class_name="w-1/3",
            ),
            rx.el.div(
                rx.text("Profundidad:"),
                rx.el.input(
                    default_value=InspectionState.inspection_depths.get(
                        vehicle_tire["id"], ""
                    ),
                    on_blur=lambda val: InspectionState.handle_depth_change(
                        vehicle_tire["id"], val, indicador
                    ),
                    class_name="w-full p-2 border rounded-md",
                    placeholder="Profundidad (mm)",
                ),
                rx.badge(InspectionState.mesaje_error_pantalla[indicador], 
                    variant="solid",
                    color_scheme="crimson", 
                    ),
                class_name="w-1/3",
            ),
            rx.el.div(
                rx.box(
                    rx.text("Estado visual:"),
                    rx.checkbox(
                    "Cortes / grietas",
                    #is_checked=InspectionState.llantas["estado_visual_checks"].contains("Cortes / grietas"),
                    on_change=lambda checked: InspectionState.estado_visual_checked(indicador, "Cortes / grietas", checked),
                    ),
                    rx.checkbox(
                    "Bultos",
                    #is_checked=InspectionState.llantas["estado_visual_checks"].contains("Bultos"),
                    on_change=lambda checked: InspectionState.estado_visual_checked(indicador, "Bultos", checked),
                    ),

                    rx.checkbox(
                    "Desgaste irregular",
    #                 is_checked="Cortes / grietas" in llanta["estado_visual_checks"],
                    on_change=lambda checked: InspectionState.estado_visual_checked(indicador, "Desgaste irregular", checked),
                    ),
                    rx.checkbox(
                    "Objeto incrustado",
    #                 is_checked="Cortes / grietas" in llanta["estado_visual_checks"],
                    on_change=lambda checked: InspectionState.estado_visual_checked(indicador, "Objeto incrustado", checked),
                    ),

                    rx.checkbox(
                    "Cambio sin Registro",
    #                 is_checked="Cortes / grietas" in llanta["estado_visual_checks"],
                    on_change=lambda checked: InspectionState.estado_visual_checked(indicador, "Cambio sin Registro", checked),
                    ),
                    
                ),       
                # rxe.mantine.multi_select(
                #     label="Comprobacion",
                #     placeholder="chequeo neumaticos",
                #     data=["Cortes / grietas", , , , ],
                #     value=InspectionState.selected_estado,
                #     on_change=InspectionState.set_selected_estado,
                # ),
                
                class_name="w-1/3",
            ),
            class_name="flex items-center justify-between gap-4 p-3 bg-gray-50 rounded-md",
        )

""" pantalla AJUSTE_PRESION
    donde solo muestra la presion a tomar"""    
def tire_ajuste_presion_row(vehicle_tire: VehicleTire, indicador: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                vehicle_tire["position"].replace("_", " ").title(),
                class_name="font-semibold",
            ),
            rx.el.p(
                f"{InspectionState.tire_vehiculo_brand.get(vehicle_tire['tire_id'], "")} {InspectionState.tire_vehiculo_size.get(vehicle_tire['tire_id'], "")}",
                class_name="text-sm text-gray-600",
            ),
            
            class_name="w-1/3",
        ),
        rx.el.div(
            rx.text("Presión(psi):"),
            rx.input(
                type="number",
                on_blur=lambda val: InspectionState.handle_presion_change(
                    vehicle_tire["id"], val
                ),
                width="100px",
            ),
            class_name="w-1/3",
        ),
        class_name="flex items-center justify-between gap-4 p-3 bg-gray-50 rounded-md",    
    )

""" pantalla ROTACION
    proceso de rotar tire, individual o grupal"""
def tire_rotacion_row(vehicle_tire: VehicleTire, indicador: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("circle-dot", size=20, color="#e91414f1"),
            rx.el.p(
                vehicle_tire["position"].replace("_", " ").title(),
                class_name="font-semibold",
            ),
            rx.el.p(
                f"{InspectionState.tire_vehiculo_brand.get(vehicle_tire['tire_id'], "")} {InspectionState.tire_vehiculo_size.get(vehicle_tire['tire_id'], "")}",
                class_name="text-sm text-gray-600",
            ),
            
            class_name="w-1/3",
        ),
        rx.el.div(
            rx.box(                 
                # rx.text("Posición Anterior:"),
                # rx.input(
                #     type="text",
                #     value=vehicle_tire["position"].replace("_", " ").title(),
                #     # on_blur=lambda val: InspectionState.handle_posicion_change(
                #     #     vehicle_tire["id"], val
                #     # ),
                #     readonly=True,
                #     width="200px",
                # ),
                rx.icon("circle-dot", size=20, color="#14e9c5f2"),
                rx.el.label("Nueva Posición:", class_name="font-medium"),
                rx.input(
                    type="text",
                    value=InspectionState.rotar_posicion_llanta[indicador],
                    # on_blur=lambda val: InspectionState.handle_presion_change(
                    #     vehicle_tire["id"], val
                    # ),
                    readonly=True,
                    width="200px",
                ),
            ),
            class_name="w-2/3",
        ),
        class_name="flex items-center justify-between gap-4 p-3 bg-gray-50 rounded-md",    
    )