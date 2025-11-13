import reflex as rx
from app.states.vehicle_state import VehicleState, Vehicle
from app.states.base_state import VehicleTire
from app.states.tire_management_state import TireManagementState


def card_vehicles(vehicle: Vehicle) -> rx.Component:
    return rx.grid(
        rx.foreach(
            rx.Var.range(3),
            lambda i: rx.card(
                rx.inset(
                    rx.image(
                        src="/reflex_banner.png",
                        width="100%",
                        height="auto",
                    ),
                    side="top",
                    pb="current",
                ),
                rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        vehicle["placa"], class_name="text-lg font-bold text-gray-800"
                    ),
                    rx.el.span(
                        f"{vehicle['marca']} {vehicle['modelo']} ({vehicle['anio']})",
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
                        rx.el.span("Registrada:"),
                        rx.el.span(vehicle["fecha_registro"], class_name="font-medium"),
                        class_name="flex justify-between text-sm",
                    ),
                    class_name="mt-4 space-y-2 text-gray-600",
                ),
             ),
        ), 
        gap="1rem",
        grid_template_columns=[
            "1fr",
            "repeat(2, 1fr)",
            "repeat(2, 1fr)",
            "repeat(3, 1fr)",
            "repeat(4, 1fr)",
        ],
    width="100%",
)

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

def card_tires(position: str, vehicle_tire: VehicleTire) -> rx.Component:
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
                            f"Instalado: {vehicle_tire['fecha_instalacion']}",
                            class_name="text-xs text-gray-500",
                        ),
                        depth_badge(vehicle_tire["profundidad_actual"]),
                        rx.el.div(
                            rx.el.button(
                                "Historia",
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