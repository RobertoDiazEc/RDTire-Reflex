import reflex as rx
import datetime


def footer() -> rx.Component:
    current_year = datetime.datetime.now().year
    return rx.box(
        rx.image(
            src="static/imagen/logoREDx1.PNG",
            alt="REDx Soluciones",
            class_name="h-26 mt-2 mb-2 rounded-full duration-300 cursor-pointer filter grayscale hover:grayscale-0",
        ),
        rx.text(
            f"© 2010-{current_year} REDx Soluciones. All rights reserved.",
            class_name="text-sm text-white",
        ),
        class_name="w-full py-1 border-t mt-8 flex justify-center items-center gap-4 bg-gradient-to-br from-[#a8b2d1] via-[#495670] to-[#0a192f] ",
    )