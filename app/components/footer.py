import reflex as rx
import datetime
from app.utils.constant import (
    FACEBOOK_URL,
    TWITTER_URL,
    INSTAGRAM_URL,
    LINKEDIN_URL,
)


def socials():
    return rx.hstack(
        rx.link(
            rx.icon("facebook", size=25),
            href=FACEBOOK_URL,
            is_external=True,
        ),  
        rx.link(
            rx.icon("message-circle", size=25),
            href=TWITTER_URL,
            is_external=True,
        ),
        rx.link(
            rx.icon("instagram", size=25),
            href=INSTAGRAM_URL,
            is_external=True,
        ),
        rx.link(
            rx.icon("linkedin", size=25),
            href=LINKEDIN_URL,
            is_external=True,
        ),
        spacing="4",
    )

# end alternate constructor
def footer() -> rx.Component:
    current_year = datetime.datetime.now().year
    return rx.el.footer(
    rx.flex(
        rx.image(
            src="static/imagen/logoREDx1.PNG",
            alt="REDx Soluciones",
            border_radius="75%",
            class_name="h-26 mt-2 mb-2 rounded-full duration-300 cursor-pointer filter grayscale hover:grayscale-0",
        ),
        rx.text(
            f"© 2010-{current_year} REDx Soluciones. All rights reserved.",
            class_name="text-sm text-white",
        ),
         socials(),
        spacing="4",
        flex_direction=["column", "column", "row"],
        width="100%",
        class_name="w-full py-1 border-t mt-8 flex justify-center items-center gap-4 bg-gradient-to-br from-[#a8b2d1] via-[#495670] to-[#0a192f] ",
    ),
   
     spacing="5",
            width="100%",
    )
    

