from django.db import models

# Modelo para el Residente
class Residente(models.Model):
    RUT = models.CharField(max_length=10, unique=True)
    DV = models.CharField(max_length=1)
    Nombres = models.CharField(max_length=100)
    Primer_Apellido = models.CharField(max_length=100)
    Segundo_Apellido = models.CharField(max_length=100, null=True, blank=True)
    Telefono = models.CharField(max_length=9)

    def __str__(self):
        rut_formato = f"{int(self.RUT):,}".replace(",", ".")
        rut_completo = f"{rut_formato}-{self.DV}"

        if self.Segundo_Apellido is None:
            segundo_apellido = ""
        else:
            segundo_apellido = self.Segundo_Apellido

        nombre_residente = f"{self.Nombres} {self.Primer_Apellido} {segundo_apellido}"
        return f"{rut_completo} | {nombre_residente}"

    class Meta:
        indexes = [
            models.Index(fields=['RUT']),  # Índice para búsquedas rápidas por RUT
            models.Index(fields=['Primer_Apellido', 'Segundo_Apellido']),  # Índice combinado para apellidos
        ]


# Modelo para el Departamento
class Departamento(models.Model):
    Codigo = models.CharField(max_length=10, unique=True)
    Residente = models.ForeignKey(Residente, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        if self.Residente is None:
            nombre_residente = "Sin Residente"
        else:
            nombre_residente = f"{self.Residente.Nombres} {self.Residente.Primer_Apellido} {self.Residente.Segundo_Apellido}"

        return f"{self.Codigo} | {nombre_residente}"

    class Meta:
        indexes = [
            models.Index(fields=['Codigo']),  # Índice para búsquedas rápidas por Código
        ]


# Modelo para el Estado
class Estado(models.Model):
    Estado = models.CharField(max_length=20, unique=True)

    def __str__(self):
        vista_estado = f"{self.id} | {self.Estado}"
        return vista_estado

    class Meta:
        indexes = [
            models.Index(fields=['Estado']),  # Índice para búsquedas rápidas por Estado
        ]


# Modelo para la Encomienda
class Encomienda(models.Model):
    Fecha_Llegada = models.DateTimeField()
    Departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=False)
    Residente = models.ForeignKey(Residente, on_delete=models.SET_NULL, null=True, blank=False)
    Fecha_Recepcion = models.DateTimeField(null=True)
    Estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=False, default=1)

    def __str__(self):
        return f"{self.id} | {self.Fecha_Llegada} | {self.Departamento.Codigo} | {self.Residente.Nombres} {self.Residente.Primer_Apellido} {self.Residente.Segundo_Apellido} | {self.Estado.Estado}"

    class Meta:
        indexes = [
            models.Index(fields=['Fecha_Llegada']),  # Índice para búsquedas rápidas por Fecha_Llegada
            models.Index(fields=['Estado']),  # Índice para búsquedas rápidas por Estado
            models.Index(fields=['Departamento', 'Residente']),  # Índice combinado para búsquedas frecuentes
        ]
