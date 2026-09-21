from django.core.management.base import BaseCommand
from django.utils import timezone
from dashboard.models import Tenant, Payment

class Command(BaseCommand):
    help = "Marking payment status as overdue for the Tenants who has not paid the rent till 7th"

    def handle(self, *args, **options):
        tenants = Tenant.objects.all()
        payments = Payment.objects.all()
        for tenant in tenants:
            if tenant.rent_status == 'pending':
                tenant.rent_status = 'overdue'

                payment = Payment.objects.get(tenant=tenant, month=timezone.now().date().replace(day=1))
                payment.penalty += 500
                
                tenant.save()
                payment.save()
        
        self.stdout.write(
            self.style.SUCCESS(
                "Payment status marked as Overdue for the Tenants who has not paid the rent till 7th"
            )
        )
        
