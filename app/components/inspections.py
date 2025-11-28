import reflex as rx
from app.states.inspections_state import InspectionState
from app.states.vehicle_state import VehicleState
from app.states.base_state import Vehicle, VehicleTire
from app.components.inspeccion_proceso import tire_inspection_row, tire_ajuste_presion_row, tire_rotacion_row


def inspection_vehicle_card(vehicle: Vehicle) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            
            rx.el.h3(
                rx.icon("truck",  color="#14e9c5f2"),
                vehicle["placa"], class_name="text-lg font-bold"),
            rx.el.p(
                f"{vehicle['marca']} {vehicle['modelo']}",
                class_name="text-sm text-gray-500",
            ),
            class_name="flex-grow",
        ),
        rx.el.button(
            f"Iniciar {InspectionState.inspeccion_valor}",
            on_click=lambda: InspectionState.open_inspection_modal(vehicle),
            class_name="mt-4 w-full bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors",
        ),
        class_name="bg-white p-4 rounded-lg border shadow-sm flex flex-col",
    )


def inspection_modal() -> rx.Component:         
    return rx.cond(
        InspectionState.show_inspection_modal
        & (InspectionState.selected_vehicle_for_inspection != None),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        f"{InspectionState.inspeccion_valor} para {InspectionState.selected_vehicle_for_inspection['placa']}",
                        class_name="text-2xl font-bold",
                    ),
                    rx.moment(InspectionState.date_now, format="YYYY-MM-DD"),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=InspectionState.close_inspection_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-start pb-4 border-b",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label("Odometro Actual ", class_name="font-medium"),
                        rx.badge(f"{InspectionState.selected_vehicle_for_inspection['odometro_actual']}",
                            color_scheme="jade", variant="soft", high_contrast=False, ),
                        rx.input(
                            #value=InspectionState.current_inspection_tiresodometro_actual,
                            #on_change=InspectionState.set_inspection_odometro,
                            placeholder="e.g. 12000",
                            type="number",
                            #class_name="w-full p-2 border rounded-md mt-1 h-24",
                        ),
                        class_name="mt-4",
                    ),
                    rx.el.div(
                        rx.cond(
                            InspectionState.inspeccion_valor == "Inspección",
                            rx.foreach(
                                InspectionState.current_inspection_tires,
                                #InspectionState.inspection_tires_by_position.keys(),
                                lambda llanta, i: tire_inspection_row(llanta, i),
                            ),
                        ),
                        rx.cond(
                            InspectionState.inspeccion_valor == "Ajuste Presión",
                            rx.foreach(
                                InspectionState.current_inspection_tires,
                                lambda llanta, i: tire_ajuste_presion_row(llanta, i),
                            ),
                        ),
                        rx.cond(
                            InspectionState.inspeccion_valor == "Rotación",
                            rx.box(
                                rx.badge(InspectionState.rotacion_item, color_scheme="green"),
                                rx.radio(["Radial", "Convencional"], on_change=InspectionState.set_rotacion_item, direction="row"),
                                rx.foreach(
                                    #InspectionState.current_inspection_tires,
                                    InspectionState.inspection_tires_by_position.keys(),
                                    lambda llanta, i: tire_rotacion_row(InspectionState.inspection_tires_by_position[llanta], i),
                                ),
                            ),
                        ),
                        class_name="space-y-3 py-4 max-h-[50vh] overflow-y-auto",
                    ),
                   
                    rx.el.div(
                        rx.el.label("Notas de Inspección", class_name="font-medium"),
                        rx.text_area(
                            value=InspectionState.inspection_notes,
                            #on_change=InspectionState.set_inspection_notes,
                            placeholder="Añadir notas sobre la inspección...",
                            #class_name="w-full p-2 border rounded-md mt-1 h-24",
                        ),
                        class_name="mt-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=InspectionState.close_inspection_modal,
                            type="button",
                            class_name="px-4 py-2 bg-gray-200 rounded-md",
                        ),
                        rx.el.button(
                            "Guardar Inspección",
                            type="submit",
                            class_name="px-4 py-2 bg-emerald-600 text-white rounded-md",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t mt-4",
                    ),
                    on_submit=lambda _: InspectionState.save_inspection(),
                ),
                class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl",
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4",
        ),
    )


def inspections_ui() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Inspección", class_name="text-3xl font-bold"),            
            rx.select(
                ["Inspección", "Ajuste Presión", "Rotación", "Montaje", "Desmontaje / Baja", "Reparacion"],
                value=InspectionState.inspeccion_valor,
                on_change=InspectionState.change_inspeccion_valor,
            ),
            
            rx.button(
                rx.icon("table-cells-split", size=20),
                rx.text("Seleccione un vehículo para iniciar ", size="3"),
                on_click=VehicleState.mostrar_vehiculos(InspectionState.cliente_id_global),
            ),

            class_name="mb-3",
        ),
        rx.el.div(
            rx.foreach(
                InspectionState.vehicles_for_inspection, inspection_vehicle_card
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6",
        ),
        inspection_modal(),
        class_name="p-4 md:p-6",
    )