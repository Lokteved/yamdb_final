from django.contrib import admin
from api.models import User
from django.apps import apps


for model in apps.get_models():
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
