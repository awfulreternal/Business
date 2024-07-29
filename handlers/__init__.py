from .start_handler import register_start_handler
from .property_handler import register_property_handler
from .business_handler import register_business_handler

def register_handlers(bot):
    register_start_handler(bot)
    register_property_handler(bot)
    register_business_handler(bot)
