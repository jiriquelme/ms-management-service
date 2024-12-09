from rest_framework import serializers
from .models import Encomienda

class EncomiendaSerializer(serializers.ModelSerializer):
    residente = serializers.SerializerMethodField()
    departamento = serializers.CharField(source='Departamento.Codigo', default='Sin información')
    estado = serializers.SerializerMethodField()

    def get_residente(self, obj):
        if obj.Residente:
            if obj.Residente.Nombres is not None:
                nombre = obj.Residente.Nombres
            else:
                nombre = ""

            if obj.Residente.Primer_Apellido is not None:
                p_apellido = obj.Residente.Primer_Apellido
            else:
                p_apellido = ""

            if obj.Residente.Segundo_Apellido is not None:
                s_apellido = obj.Residente.Segundo_Apellido
            else:
                s_apellido = ""
            
            nombre_completo = f"{nombre} {p_apellido} {s_apellido}".strip()

            return nombre_completo
        return "Sin información"

    def get_estado(self, obj):
        return "Entregado" if obj.Fecha_Recepcion else "Pendiente"

    class Meta:
        model = Encomienda
        fields = ['id', 'Fecha_Llegada', 'Fecha_Recepcion', 'departamento', 'residente', 'estado']
