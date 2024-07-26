from django.contrib import admin

# Register your models here.
# @action(detail=True, methods=["post"], permission_classes=[IsAdminUser])
# def approve_request(self, request):
#     obj: CreditRequest = self.get_object()

#     if obj.approved:
#         return Response(status=status.HTTP_400_BAD_REQUEST)

#     with transaction.atomic():
#         try:
#             obj.approved = True
#             obj.save()

#             vendor_obj = Vendor.objects.select_for_update().get(id=obj.vendor_id)
#             vendor_obj.balance += obj.amount
#             vendor_obj.save()
#         except:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     return Response(status=status.HTTP_200_OK)
