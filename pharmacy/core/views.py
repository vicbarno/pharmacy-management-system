from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Medicine, Patient, Sale, SaleItem
from .serializers import MedicineSerializer, PatientSerializer, SaleSerializer, SaleItemSerializer


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer

    @action(detail=True, methods=['post'])
    def update_stock(self, request, pk=None):
        medicine = self.get_object()
        quantity_change = request.data.get('quantity_change', 0)
        medicine.quantity += int(quantity_change)
        medicine.save()
        serializer = self.get_serializer(medicine)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        threshold = request.query_params.get('threshold', 10)
        medicines = Medicine.objects.filter(quantity__lte=threshold)
        serializer = self.get_serializer(medicines, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expired(self, request):
        from django.utils import timezone
        medicines = Medicine.objects.filter(expiry_date__lt=timezone.now().date())
        serializer = self.get_serializer(medicines, many=True)
        return Response(serializer.data)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-created_at')
    serializer_class = SaleSerializer

    @action(detail=False, methods=['post'])
    def create_sale(self, request):
        patient_id = request.data.get('patient_id')
        items_data = request.data.get('items', [])

        if not items_data:
            return Response({'error': 'No items provided'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # Create sale
            sale = Sale.objects.create(patient_id=patient_id, total=0)

            total = 0
            for item_data in items_data:
                medicine_id = item_data['medicine_id']
                quantity = item_data['quantity']

                medicine = Medicine.objects.get(id=medicine_id)
                if medicine.quantity < quantity:
                    return Response({'error': f'Insufficient stock for {medicine.name}'}, status=status.HTTP_400_BAD_REQUEST)

                # Create sale item
                SaleItem.objects.create(sale=sale, medicine=medicine, quantity=quantity)

                # Update medicine stock
                medicine.quantity -= quantity
                medicine.save()

                total += medicine.price * quantity

            sale.total = total
            sale.save()

        serializer = self.get_serializer(sale)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SaleItemViewSet(viewsets.ModelViewSet):
    queryset = SaleItem.objects.all()
    serializer_class = SaleItemSerializer
