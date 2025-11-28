import reflex as rx
from app.utils.campos import clickable_area_button
from app.states.tire_management_state import TireManagementState

def clickable_area(top: str, bottom: str, left: str, right: str, 
                   width: str, height: str, target_route: str) -> rx.Component:
    """
    Crea un área clickeable transparente y la posiciona de forma absoluta.
    """
    # El rx.link será tu área clickeable
    return rx.link(
        "", # Contenido vacío
        href=target_route,
        style={
            "position": "absolute",
            "top": top,
            "bottom": bottom,
            "left": left,
            "right": right,
            "width": width,
            "height": height,
            "cursor": "pointer",
            
            # CRÍTICO: Haz el área transparente. Puedes usar un color de fondo temporal
            # como "rgba(255, 0, 0, 0.3)" durante el desarrollo para verificar la posición.
            "background_color": "transparent", 
            "border": "1px solid transparent", # Manten el borde transparente
            "z_index": 10 # Asegura que esté sobre la imagen
        }
    )


def image_map_view() -> rx.Component:
    return rx.box(
         rx.image(
                src="/static/imagen/llanta_2eje_4llantas.png",
                alt="Mapa de Imagen con Áreas Clickeables",
                width="300px",
                height="400px",
            ),
        
        # 2. Puntos Clickeables Superpuestos
        clickable_area_button("10%", "auto", "20%", "auto", "150px", "100px",
            TireManagementState.posicion_llanta_imagen("delantera_izquierda")
        ),

        clickable_area_button(
            "50%", "auto", "20%", "auto", "150px", "100px",
             TireManagementState.posicion_llanta_imagen("delantera_derecha")
        ),
        # ... y así sucesivamente para las 4 áreas ...
        # 1. Contenedor Principal (Define el tamaño del mapa)
        width="300px", 
        height="400px",
        position="relative", # ¡CRÍTICO! Permite posicionar elementos 'absolute' dentro.
        
        border="2px solid #ccc",
        border_radius="8px",
        overflow="hidden",
    )