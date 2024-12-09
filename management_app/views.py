# ========================================================================
#                                Imports
# ========================================================================

from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.views.generic import ListView
from django.utils import timezone
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework import status
from .models import Residente, Departamento, Encomienda, Estado
from .serializers import EncomiendaSerializer
import json

# ========================================================================
#                                  Endpoints
# ========================================================================

class ObtenerEstadoEncomiendaView(APIView):
    def get(self, request, encomienda_id):
        try:
            # Buscar la encomienda por ID
            encomienda = Encomienda.objects.get(id=encomienda_id)
            # Retornar el estado de la encomienda
            return Response({"estado": encomienda.Estado.Estado}, status=status.HTTP_200_OK)
        except Encomienda.DoesNotExist:
            # Manejar caso donde no exista la encomienda
            return Response({"error": "Encomienda no encontrada"}, status=status.HTTP_404_NOT_FOUND)


class ObtenerResidenteView(APIView):
    def get(self, request):
        try:
            codigo_departamento = request.query_params.get("codigo_departamento")

            if not codigo_departamento:
                return Response({"error": "El código de departamento son requeridos"}, status=400)

            departamento = get_object_or_404(Departamento, Codigo=codigo_departamento)
            #departamento = Departamento.objects.get_object_or_404(Departamento, Codigo=codigo_departamento)
            residente = departamento.Residente

            if not residente:
                return Response({"error": "Departamento no tiene residente"}, status=400)

            data = {
                "id": residente.id,
                "rut": residente.RUT,
                "rut_dv":f"{residente.RUT}-{residente.DV}",
                "nombre_completo": f"{residente.Nombres} {residente.Primer_Apellido} {residente.Segundo_Apellido}",
                "telefono": residente.Telefono
            }
            return Response(data)

        except Http404:
            return Response({"error": "Departamento no existe"}, status=404)

        except Exception as e:
            error = str(e).replace("\n"," | ")

            print(f"Error: {error}")
            return Response({"error": error}, status=404)

class RegistrarEncomiendaView(APIView):
    def post(self, request):
        departamento_id = request.data.get("departamento_id")
        residente_id = request.data.get("residente_id")
        fecha_llegada = timezone.now()  # Fecha de llegada como el momento actual

        if not departamento_id or not residente_id:
            return Response({"error": "Departamento y residente son requeridos"}, status=400)

        try:
            departamento = Departamento.objects.get(Codigo=departamento_id)
            residente = Residente.objects.get(id=residente_id)
            estado = Estado.objects.get(id=1)  # Estado inicial predeterminado

            # Crear el registro de encomienda
            encomienda = Encomienda.objects.create(
                Fecha_Llegada=fecha_llegada,
                Departamento=departamento,
                Residente=residente,
                Estado=estado
            )
            return Response({"status": "Encomienda registrada", "id": encomienda.id})
        except Departamento.DoesNotExist:
            return Response({"error": "Departamento no encontrado"}, status=404)
        except Residente.DoesNotExist:
            return Response({"error": "Residente no encontrado"}, status=404)

class AnalizarQRView(APIView):
    def post(self, request):
        qr_data = request.data.get("qr_data")  # El contenido del QR escaneado

        if not qr_data:
            return Response({"error": "Datos del QR requeridos"}, status=400)

        try:
            # Identificar la encomienda basada en los datos del QR
            encomienda = Encomienda.objects.get(id=qr_data)  # Asume que el QR tiene el ID de la encomienda

            # Cambiar el estado a "Entregado"
            estado_entregado = Estado.objects.get(id=2)  # Ajusta según el nombre exacto en tu BD
            encomienda.Estado = estado_entregado
            encomienda.Fecha_Recepcion = timezone.now()  # Registrar la fecha de recepción
            encomienda.save()

            return Response({"status": "Encomienda marcada como entregada", "id": encomienda.id})
        except Encomienda.DoesNotExist:
            return Response({"error": "Encomienda no encontrada"}, status=404)
        except Estado.DoesNotExist:
            return Response({"error": "Estado 'Entregado' no encontrado"}, status=500)
        


class EncomiendaEndView(ListAPIView):
    queryset = Encomienda.objects.select_related('Departamento', 'Residente', 'Estado').all().order_by('-Fecha_Llegada')
    serializer_class = EncomiendaSerializer

    
# ========================================================================
#                                CRUD
# ========================================================================

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Vistas para Residente
class ResidenteListView(ListView):
    model = Residente
    template_name = "lista_dinamica.html"
    context_object_name = "datos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Lista de Residentes"
        context["modelo"] = "residente"
        return context


class ResidenteCreateView(CreateView):
    model = Residente
    fields = ["RUT", "DV", "Nombres", "Primer_Apellido", "Segundo_Apellido", "Telefono"]
    template_name = "formulario.html"
    success_url = reverse_lazy("lista_residentes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar nombre del modelo al contexto
        context["model_name"] = self.model._meta.verbose_name
        return context


class ResidenteUpdateView(UpdateView):
    model = Residente
    fields = ["RUT", "DV", "Nombres", "Primer_Apellido", "Segundo_Apellido", "Telefono"]
    template_name = "formulario.html"
    success_url = reverse_lazy("lista_residentes")


class ResidenteDeleteView(DeleteView):
    model = Residente
    template_name = "confirmar_eliminacion.html"
    success_url = reverse_lazy("lista_residentes")

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class DepartamentoListView(ListView):
    model = Departamento
    template_name = "lista_dinamica.html"
    context_object_name = "datos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Lista de Departamentos"
        context["modelo"] = "departamento"
        return context


class DepartamentoCreateView(CreateView):
    model = Departamento
    fields = ["Codigo", "Residente"]
    template_name = "formulario.html"
    success_url = reverse_lazy("lista_departamentos")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar nombre del modelo al contexto
        context["model_name"] = self.model._meta.verbose_name
        return context

class DepartamentoUpdateView(UpdateView):
    model = Departamento
    fields = ["Codigo", "Residente"]
    template_name = "formulario.html"
    success_url = reverse_lazy("lista_departamentos")


class DepartamentoDeleteView(DeleteView):
    model = Departamento
    template_name = "confirmar_eliminacion.html"
    success_url = reverse_lazy("lista_departamentos")

# Vistas para Encomienda
class EncomiendaListView(ListView):
    model = Encomienda
    template_name = "lista_dinamica.html"
    context_object_name = "datos"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Lista de Encomiendas"
        context["modelo"] = "encomienda"
        return context


class EncomiendaCreateView(CreateView):
    model = Encomienda
    fields = ['Fecha_Llegada', 'Departamento', 'Residente', 'Fecha_Recepcion', 'Estado']
    template_name = 'formulario.html'
    success_url = reverse_lazy('lista_encomiendas')

    def get_form(self):
        form = super().get_form()
        form.fields['Fecha_Llegada'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        form.fields['Fecha_Recepcion'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})
        return form


class EncomiendaUpdateView(UpdateView):
    model = Encomienda
    fields = ["Fecha_Llegada", "Departamento", "Residente", "Fecha_Recepcion", "Estado"]
    template_name = "formulario.html"
    success_url = reverse_lazy("lista_encomiendas")


class EncomiendaDeleteView(DeleteView):
    model = Encomienda
    template_name = "confirmar_eliminacion.html"
    success_url = reverse_lazy("lista_encomiendas")



# ========================================================================
#                                Renders
# ========================================================================


@csrf_exempt
def eliminar_encomiendas_seleccionadas(request):
    if request.method == "POST":
        try:
            # Decodificar los datos enviados
            data = json.loads(request.body)
            ids = data.get("ids", [])

            # Validar si hay IDs para eliminar
            if not ids:
                return JsonResponse({"error": "No se proporcionaron IDs para eliminar."}, status=400)

            # Eliminar las encomiendas correspondientes
            Encomienda.objects.filter(id__in=ids).delete()

            return JsonResponse({"message": "Encomiendas eliminadas con éxito."}, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Método no permitido."}, status=405)

def render_pagina_principal(request):
    return render(request, "index.html")

def lista_dinamica(request, modelo):
    if modelo == 'residente':
        datos = Residente.objects.all()
        titulo = "Lista de Residentes"
    elif modelo == 'departamento':
        datos = Departamento.objects.all()
        titulo = "Lista de Departamentos"
    elif modelo == 'encomienda':
        datos = Encomienda.objects.all()
        titulo = "Lista de Encomiendas"

        # Agregar estilos al estado
        for item in datos:
            if item.Estado.Estado == 'Pendiente':
                item.estado_clase = 'estado-pendiente'
            elif item.Estado.Estado == 'Entregado':
                item.estado_clase = 'estado-entregado'
    else:
        datos = []
        titulo = "No se encontraron datos"

    contexto = {
        'datos': datos,
        'titulo': titulo,
        'modelo': modelo
    }

    return render(request, 'lista_dinamica.html', contexto)

