# management_app/urls.py

from django.urls import path
from .views import ObtenerResidenteView, RegistrarEncomiendaView, AnalizarQRView, ResidenteListView, ResidenteCreateView, ResidenteUpdateView, ResidenteDeleteView, DepartamentoListView, DepartamentoCreateView, DepartamentoUpdateView, DepartamentoDeleteView,    EncomiendaListView, EncomiendaCreateView, EncomiendaUpdateView, EncomiendaDeleteView, eliminar_encomiendas_seleccionadas, ObtenerEstadoEncomiendaView

urlpatterns = [
    path('residente/', ObtenerResidenteView.as_view(), name='obtener-residente'),
    path('registrar-encomienda/', RegistrarEncomiendaView.as_view(), name='registrar-encomienda'),
    path('analizar-qr/', AnalizarQRView.as_view(), name='analizar-qr'),
    path('eliminar-encomiendas-seleccionadas/', eliminar_encomiendas_seleccionadas, name='eliminar_encomiendas_seleccionadas'),
    path('encomienda/<int:encomienda_id>/estado/', ObtenerEstadoEncomiendaView.as_view(), name='estado-encomienda'),

        # CRUD para Residente
    path("residente-crud/", ResidenteListView.as_view(), name="lista_residentes"),
    path("residente-crud/crear/", ResidenteCreateView.as_view(), name="crear_residente"),
    path("residente-crud/editar/<int:pk>/", ResidenteUpdateView.as_view(), name="editar_residente"),
    path("residente-crud/eliminar/<int:pk>/", ResidenteDeleteView.as_view(), name="eliminar_residente"),

    # CRUD para Departamento
    path("departamento-crud/", DepartamentoListView.as_view(), name="lista_departamentos"),
    path("departamento-crud/crear/", DepartamentoCreateView.as_view(), name="crear_departamento"),
    path("departamento-crud/editar/<int:pk>/", DepartamentoUpdateView.as_view(), name="editar_departamento"),
    path("departamento-crud/eliminar/<int:pk>/", DepartamentoDeleteView.as_view(), name="eliminar_departamento"),

    # CRUD para Encomienda
    path("encomienda-crud/", EncomiendaListView.as_view(), name="lista_encomiendas"),
    path("encomienda-crud/crear/", EncomiendaCreateView.as_view(), name="crear_encomienda"),
    path("encomienda-crud/editar/<int:pk>/", EncomiendaUpdateView.as_view(), name="editar_encomienda"),
    path("encomienda-crud/eliminar/<int:pk>/", EncomiendaDeleteView.as_view(), name="eliminar_encomienda"),
]