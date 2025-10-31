import reflex as rx
from app.states.tire_management_state import TireManagementState
from app.states.vehicle_state import VehicleState, Vehicle
from app.states.base_state import Tire, VehicleTire, TireHistory


def vehicle_card(vehicle: Vehicle) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    vehicle["placa"], class_name="text-lg font-bold text-gray-800"
                ),
                rx.el.span(
                    f"{vehicle['marca']} {vehicle['modelo']} ({vehicle['ano']})",
                    class_name="text-gray-500",
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: VehicleState.open_edit_vehicle_modal(vehicle),
                    class_name="p-2 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded-md",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: VehicleState.delete_vehicle(vehicle["id"]),
                    class_name="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded-md",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-start justify-between",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span("Type:"),
                rx.el.span(vehicle["tipo"], class_name="font-medium"),
                class_name="flex justify-between text-sm",
            ),
            rx.el.div(
                rx.el.span("Registered:"),
                rx.el.span(vehicle["fecha_registro"], class_name="font-medium"),
                class_name="flex justify-between text-sm",
            ),
            class_name="mt-4 space-y-2 text-gray-600",
        ),
        on_click=lambda: TireManagementState.open_vehicle_detail(vehicle["id"]),
        class_name="bg-white p-4 rounded-lg border border-gray-200 shadow-sm hover:shadow-md transition-shadow cursor-pointer",
    )


def vehicle_modal() -> rx.Component:
    def form_field(
        label: str,
        name: str,
        value: rx.Var,
        on_change: rx.event.EventHandler,
        placeholder: str,
        type: str = "text",
    ) -> rx.Component:
        return rx.el.div(
            rx.el.label(label, class_name="text-sm font-medium"),
            rx.el.input(
                placeholder=placeholder,
                name=name,
                type=type,
                default_value=value,
                on_change=on_change,
                class_name="w-full p-2 border rounded-md mt-1",
            ),
            class_name="flex-1",
        )

    return rx.cond(
        VehicleState.show_vehicle_modal,
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        rx.cond(
                            VehicleState.is_editing_vehicle,
                            "Editar Vehículo",
                            "Nuevo Vehículo",
                        ),
                        class_name="text-xl font-bold",
                    ),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=VehicleState.close_vehicle_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-center pb-4 border-b",
                ),
                rx.el.form(
                    rx.el.div(
                        form_field(
                            "License Plate",
                            "placa",
                            VehicleState.new_vehicle["placa"],
                            lambda val: VehicleState.handle_vehicle_change(
                                "placa", val
                            ),
                            "e.g. PCJ-1234",
                        ),
                        form_field(
                            "Brand",
                            "marca",
                            VehicleState.new_vehicle["marca"],
                            lambda val: VehicleState.handle_vehicle_change(
                                "marca", val
                            ),
                            "e.g. Toyota",
                        ),
                        form_field(
                            "Model",
                            "modelo",
                            VehicleState.new_vehicle["modelo"],
                            lambda val: VehicleState.handle_vehicle_change(
                                "modelo", val
                            ),
                            "e.g. Hilux",
                        ),
                        form_field(
                            "Year",
                            "ano",
                            VehicleState.new_vehicle["ano"].to_string(),
                            lambda val: VehicleState.handle_vehicle_change("ano", val),
                            "e.g. 2022",
                            type="number",
                        ),
                        form_field(
                            "Type",
                            "tipo",
                            VehicleState.new_vehicle["tipo"],
                            lambda val: VehicleState.handle_vehicle_change("tipo", val),
                            "e.g. Truck",
                        ),
                        class_name="grid grid-cols-1 md:grid-cols-2 gap-4 py-4",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=VehicleState.close_vehicle_modal,
                            class_name="px-4 py-2 bg-gray-200 rounded-md",
                            type="button",
                        ),
                        rx.el.button(
                            "Grabar",
                            type="submit",
                            class_name="px-4 py-2 bg-emerald-600 text-white rounded-md",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t",
                    ),
                    on_submit=VehicleState.save_vehicle,
                ),
                class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-2xl",
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50",
        ),
    )


def vehicle_detail_modal() -> rx.Component:
    def depth_badge(depth: float) -> rx.Component:
        return rx.cond(
            depth <= 1.03,
            rx.el.span(
                f"{depth:.2f} mm",
                class_name="px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full w-fit",
            ),
            rx.cond(
                depth <= 3.0,
                rx.el.span(
                    f"{depth:.2f} mm",
                    class_name="px-2 py-1 text-xs font-semibold text-yellow-800 bg-yellow-100 rounded-full w-fit",
                ),
                rx.el.span(
                    f"{depth:.2f} mm",
                    class_name="px-2 py-1 text-xs font-semibold text-emerald-800 bg-emerald-100 rounded-full w-fit",
                ),
            ),
        )

    def get_tire_card(position: str, vehicle_tire: VehicleTire | None) -> rx.Component:
        return rx.el.div(
            rx.el.div(
                rx.el.p(
                    position.replace("_", " ").title(),
                    class_name="font-bold capitalize",
                ),
                rx.cond(
                    vehicle_tire,
                    rx.el.div(
                        rx.el.p(
                            f"{TireManagementState.tire_info_by_id.get(vehicle_tire['tire_id'], {}).get('brand', 'N/A')} {TireManagementState.tire_info_by_id.get(vehicle_tire['tire_id'], {}).get('model', 'N/A')}",
                            class_name="text-sm font-medium",
                        ),
                        rx.el.p(
                            f"Installed: {vehicle_tire['fecha_instalacion']}",
                            class_name="text-xs text-gray-500",
                        ),
                        depth_badge(vehicle_tire["profundidad_actual"]),
                        rx.el.div(
                            rx.el.button(
                                "History",
                                on_click=lambda: TireManagementState.open_tire_history_modal(
                                    vehicle_tire["id"]
                                ),
                                class_name="text-xs text-blue-600 hover:underline",
                            ),
                            rx.el.button(
                                "Remove",
                                on_click=lambda: TireManagementState.remove_tire_from_vehicle(
                                    vehicle_tire["id"]
                                ),
                                class_name="text-xs text-red-600 hover:underline",
                            ),
                            class_name="flex gap-2 mt-2",
                        ),
                        class_name="mt-2 space-y-1",
                    ),
                    rx.el.button(
                        "Nuevo",
                        on_click=lambda: TireManagementState.open_add_tire_to_vehicle_modal(
                            TireManagementState.selected_vehicle_for_detail["id"],
                            position,
                        ),
                        class_name="mt-2 w-full bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm py-2 px-3 rounded-md",
                    ),
                ),
                class_name="p-4 border rounded-lg h-full flex flex-col justify-between",
            )
        )

    return rx.cond(
        TireManagementState.show_vehicle_detail_modal
        & (TireManagementState.selected_vehicle_for_detail != None),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h2(
                            f"{TireManagementState.selected_vehicle_for_detail.get('marca', 'N/A')} {TireManagementState.selected_vehicle_for_detail.get('modelo', 'N/A')}",
                            class_name="text-2xl font-bold",
                        ),
                        rx.el.p(
                            TireManagementState.selected_vehicle_for_detail.get(
                                "placa", ""
                            ),
                            class_name="text-gray-500",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=TireManagementState.close_vehicle_detail,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-start pb-4 border-b",
                ),
                rx.el.div(
                    rx.foreach(
                        TireManagementState.vehicle_tires_by_position.keys(),
                        lambda position: get_tire_card(
                            position,
                            TireManagementState.vehicle_tires_by_position[position],
                        ),
                    ),
                    class_name="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 py-6",
                ),
                class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-6xl",
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4",
        ),
        None,
    )


def add_tire_to_vehicle_modal() -> rx.Component:
    return rx.cond(
        TireManagementState.show_add_tire_modal,
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    f"Añadir LLanta para {TireManagementState.new_vehicle_tire['position'].replace('_', ' ').title()}",
                    class_name="text-xl font-bold",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label("Selecionar Llanta", class_name="font-medium"),
                        rx.el.select(
                            rx.foreach(
                                TireManagementState.tires,
                                lambda tire: rx.el.option(
                                    f"{tire['brand']} {tire['model']} ({tire['size']})",
                                    value=tire["id"].to_string(),
                                ),
                            ),
                            name="tire_id",
                            on_change=lambda val: TireManagementState.handle_new_vehicle_tire_change(
                                "tire_id", val
                            ),
                            class_name="w-full p-2 border rounded-md mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Fecha de Instalacion", class_name="font-medium"),
                        rx.el.input(
                            type="date",
                            name="fecha_instalacion",
                            class_name="w-full p-2 border rounded-md mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Profundidad Inicial (mm)", class_name="font-medium"),
                        rx.el.input(
                            type="number",
                            default_value="8.0",
                            name="profundidad_actual",
                            class_name="w-full p-2 border rounded-md mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Estado Inicial", class_name="font-medium"),
                        rx.el.select(
                            rx.el.option("Nueva", value="Nueva"),
                            rx.el.option("En uso", value="En uso"),
                            name="estado",
                            on_change=lambda val: TireManagementState.handle_new_vehicle_tire_change(
                                "estado", val
                            ),
                            class_name="w-full p-2 border rounded-md mt-1",
                        ),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            on_click=TireManagementState.close_add_tire_to_vehicle_modal,
                            type="button",
                            class_name="px-4 py-2 bg-gray-200 rounded-md",
                        ),
                        rx.el.button(
                            "Grabar",
                            type="submit",
                            class_name="px-4 py-2 bg-emerald-600 text-white rounded-md",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t mt-4",
                    ),
                    on_submit=TireManagementState.save_tire_to_vehicle,
                    class_name="space-y-4 py-4",
                ),
                class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-md",
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50",
        ),
    )


def tire_history_modal() -> rx.Component:
    def depth_badge(depth: float) -> rx.Component:
        return rx.cond(
            depth <= 1.03,
            rx.el.span(
                f"{depth:.2f} mm",
                class_name="px-2 py-1 text-xs font-semibold text-red-800 bg-red-100 rounded-full w-fit",
            ),
            rx.cond(
                depth <= 3.0,
                rx.el.span(
                    f"{depth:.2f} mm",
                    class_name="px-2 py-1 text-xs font-semibold text-yellow-800 bg-yellow-100 rounded-full w-fit",
                ),
                rx.el.span(
                    f"{depth:.2f} mm",
                    class_name="px-2 py-1 text-xs font-semibold text-emerald-800 bg-emerald-100 rounded-full w-fit",
                ),
            ),
        )

    def history_row(history_item: TireHistory) -> rx.Component:
        return rx.el.tr(
            rx.el.td(history_item["fecha"], class_name="p-2"),
            rx.el.td(history_item["tipo_evento"], class_name="p-2"),
            rx.el.td(
                rx.cond(
                    history_item["profundidad_medida"] != None,
                    depth_badge(history_item["profundidad_medida"]),
                    "N/A",
                ),
                class_name="p-2",
            ),
            rx.el.td(history_item.get("notas", ""), class_name="p-2"),
        )

    return rx.cond(
        TireManagementState.show_tire_history_modal
        & (TireManagementState.tire_info_for_history != None),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        f"History for {TireManagementState.tire_info_for_history.get('brand', 'N/A')} {TireManagementState.tire_info_for_history.get('model', 'N/A')}",
                        class_name="text-xl font-bold",
                    ),
                    rx.el.button(
                        rx.icon("x"),
                        on_click=TireManagementState.close_tire_history_modal,
                        class_name="p-1 rounded-full hover:bg-gray-100",
                    ),
                    class_name="flex justify-between items-center pb-4 border-b",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th("Date", class_name="p-2 text-left"),
                                rx.el.th("Event", class_name="p-2 text-left"),
                                rx.el.th("Depth", class_name="p-2 text-left"),
                                rx.el.th("Notes", class_name="p-2 text-left"),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                TireManagementState.history_for_selected_tire,
                                history_row,
                            )
                        ),
                    ),
                    class_name="w-full overflow-y-auto max-h-[60vh] mt-4",
                ),
                class_name="bg-white rounded-lg shadow-xl p-6 w-full max-w-3xl",
            ),
            class_name="fixed inset-0 bg-black/50 flex items-center justify-center z-50",
        ),
        None,
    )


def vehicles_page_ui() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1("Mantenimieto Vehículo", class_name="text-3xl font-bold"),
            rx.el.p(
                "Registre y gestione su flota de vehículos",
                class_name="text-gray-500 mt-1",
            ),
            rx.el.button(
                "Nuevo Vehículo",
                on_click=VehicleState.open_add_vehicle_modal,
                class_name="mt-4 bg-emerald-600 text-white px-4 py-2 rounded-lg hover:bg-emerald-700",
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.foreach(VehicleState.vehicles, vehicle_card),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6",
        ),
        vehicle_modal(),
        vehicle_detail_modal(),
        add_tire_to_vehicle_modal(),
        tire_history_modal(),
        class_name="p-4 md:p-6",
    )