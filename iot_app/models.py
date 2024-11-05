from django.db import models
import uuid
# Create your models here.
import uuid
from django.db import models

class Users(models.Model):
    """Tabela de usuários."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Cattle(models.Model):
    """Tabela de gado."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    RFID = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])
    birth_date = models.DateField()
    description = models.CharField(max_length=500, blank=True, null=True)
    birth_weight = models.DecimalField(max_digits=5, decimal_places=2)
    weaning_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    slaughter_weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    father = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='father_cattle')
    mother = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='mother_cattle')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cattle {self.id}"


class Fertility(models.Model):
    """Tabela de fertilidade do gado."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    insemination_date = models.DateField()
    insemination_result_date = models.DateField(blank=True, null=True)
    insemination_result = models.BooleanField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fertility record for {self.cattle}"


class Vaccination(models.Model):
    """Tabela de vacinação do gado."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Vaccination {self.vaccine_name} for {self.cattle}"


class RfidMetrics(models.Model):
    """Tabela de métricas RFID do gado."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cattle = models.ForeignKey(Cattle, on_delete=models.CASCADE)
    activation_time = models.DateTimeField()
    deactivation_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"RFID Metrics for {self.cattle}"
