from django.core.management.base import BaseCommand
from django.utils import timezone

from dashboard.models import Tenant, Payment

import razorpay
from django.conf import settings

class Command(BaseCommand):
    help = "Create monthly payment records for active tenants"

    def handle(self, *args, **kwargs):
        current_month = timezone.now().date().replace(day=1)

        tenants = Tenant.objects.filter(status="active")

        for tenant in tenants:
            amount = tenant.room.rent

            payment, created= Payment.objects.get_or_create(
                tenant=tenant,
                month=current_month,
                defaults={
                    "rent_amount": amount,
                    "advance_used": 0,
                    "penalty": 0,
                    "total_amount": amount,
                    "status": "pending"
                }
            )

            if created:
                client = razorpay.Client(
                    auth=(
                        settings.RAZORPAY_KEY_ID,
                        settings.RAZORPAY_KEY_SECRET
                    )
                )
        
                order_data = {
                    "amount" : amount * 100,
                    "currency": "INR",
                    "receipt": f"rent_{tenant.firstname}_{timezone.now().timestamp()}"
                }
            
                order = client.order.create(data=order_data)
        
                payment.razorpay_order_id = order["id"]
                payment.save()

            tenant.rent_status = "pending"
            tenant.save()


        self.stdout.write(
            self.style.SUCCESS(
                "Monthly Payment records created successfully."
            )
        )