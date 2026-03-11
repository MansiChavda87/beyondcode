from django.core.management.base import BaseCommand
from marketing.models import Footer


class Command(BaseCommand):
    help = 'Fix footer links to point to correct URLs'

    def handle(self, *args, **options):
        self._fix_footer_links()
        self.stdout.write(self.style.SUCCESS('Footer links updated successfully.'))

    def _fix_footer_links(self):
        footer, created = Footer.objects.update_or_create(
            label='Default',
            defaults={
                'columns_json': [
                    {
                        'title': 'Links',
                        'links': [
                            {'label': 'Privacy Notice', 'url': '/privacy/'},
                            {'label': 'Terms of Use', 'url': '/terms/'},
                            {'label': 'Sitemap', 'url': '/sitemap.xml'},
                            {'label': 'Contact Us', 'url': '/contact/'},
                        ],
                    },
                ],
                'cta_title': 'Ready to streamline your collections?',
                'cta_body': 'Start your free 14-day trial. No credit card required.',
                'cta_button_label': 'Get Started Free',
                'cta_button_url': '/contact/',
                'legal_text': (
                    'BeyondCode AI is a technology platform. '
                    'This is example disclaimer text for your application.'
                ),
            },
        )
        action = 'created' if created else 'updated'
        self.stdout.write(f'  Footer {action}.')