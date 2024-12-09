from django.contrib import admin
from .models import Residente, Departamento, Encomienda, Estado

# Register your models here.
admin.site.register(Residente)
admin.site.register(Departamento)
admin.site.register(Encomienda)
admin.site.register(Estado)

