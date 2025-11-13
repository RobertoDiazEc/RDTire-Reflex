import reflex as rx
from app.states.inspections_state import InspectionState
from app.states.base_state import Vehicle, VehicleTire


def inspection_vehicle_card(vehicle: Vehicle) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(vehicle["placa"], class_name="text-lg font-bold"),
            rx.el.p(
                f"{vehicle['marca']} {vehicle['modelo']}",
                class_name="text-sm text-gray-500",
            ),
            class_name="flex-grow",
        ),
        rx.el.button(
            "Iniciar Inspección",
            on_click=lambda: InspectionState.open_inspection_modal(vehicle),
            class_name="mt-4 w-full bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700 transition-colors",
        ),
        class_name="bg-white p-4 rounded-lg border shadow-sm flex flex-col",
    )


def inspection_modal() -> rx.Component:
    def tire_inspection_row(vehicle_tire: VehicleTire) -> rx.Component:
        tire_info = InspectionState.tire_info_by_id.get(vehicle_tire["tire_id"], {})
        return rx.el.div(
            rx.el.div(
                rx.el.p(
                    vehicle_tire["position"].replace("_", " ").title(),
                    class_name="font-semibold",
                ),
                rx.el.p(
                    f"{tire_info.get('brand', 'N/A')} {tire_info.get('model', 'N/A')}",
                    class_name="text-sm text-gray-600",
                ),
                class_name="w-1/3",
            ),
            rx.el.div(
                rx.el.input(
                    type="number",
                    default_value=InspectionState.inspection_depths.get(
                        vehicle_tire["id"], ""
                    ),
                    on_change=lambda val: InspectionState.handle_depth_change(
                        vehicle_tire["id"], val
                    ),
                    class_name="w-full p-2 border rounded-md",
                    placeholder="Profundidad (mm)",
                ),
                class_name="w-1/3",
            ),
            class_name="flex items-center justify-between gap-4 p-3 bg-gray-50 rounded-md",
        )

    return rx.cond(
        InspectionState.show_inspection_modal
        & (InspectionState.selected_vehicle_for_inspection != None),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        f"Inspección para {InspectionState.selected_vehicle_for_inspection['placa']}",
                        class_name="text-2xl font-bold",
                    ),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=InspectionState.close_inspection_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-start pb-4 border-b",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.foreach(
                            InspectionState.current_inspection_tires,
                            tire_inspection_row,
                        ),
                        class_name="space-y-3 py-4 max-h-[50vh] overflow-y-auto",
                    ),
                    rx.el.div(
                        rx.el.label("Notas de Inspección", class_name="font-medium"),
                        rx.text_area(
                            on_change=InspectionState.set_inspection_notes,
                            placeholder="Añadir notas sobre la inspección...",
                            class_name="w-full p-2 border rounded-md mt-1 h-24",
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
            rx.el.p(
                "Seleccione un vehículo para iniciar la inspección de llantas.",
                class_name="text-gray-500 mt-1",
            ),
            class_name="mb-6",
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