from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Seed CMS Admins group and initial admin membership'

    def handle(self, *args, **options):
        group, _ = Group.objects.get_or_create(name='CMS Admins')
        User = get_user_model()
        user = User.objects.filter(email=os.getenv('CMS_ADMIN_EMAIL', '')).first()
        if not user:
            self.stdout.write(self.style.WARNING('CMS admin user not found'))
            return
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS('Seeded CMS Admins group'))