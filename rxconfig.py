import os       
import reflex as rx
import reflex_enterprise as rxe
from decouple import config

DATABASE_URL = config("DATABASE_URL")


config = rx.Config(
    app_name="app", 
    plugins=[
        rx.plugins.TailwindV4Plugin(),
    ],
    disable_plugins =['reflex.plugins.sitemap.SitemapPlugin'],
    db_url=DATABASE_URL,
    )
