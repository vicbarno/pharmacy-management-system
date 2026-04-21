from rest_framework import serializers
from .models import Medicine, Patient, Sale, SaleItem


class MedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicine
        fields = "__all__"


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__"


class SaleItemSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    medicine_price = serializers.DecimalField(source='medicine.price', max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = SaleItem
        fields = ['id', 'medicine', 'medicine_name', 'medicine_price', 'quantity', 'subtotal']

    def get_subtotal(self, obj):
        return obj.quantity * obj.medicine.price


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(source='saleitem_set', many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.name', read_only=True)

    class Meta:
        model = Sale
        fields = ['id', 'patient', 'patient_name', 'total', 'created_at', 'items']