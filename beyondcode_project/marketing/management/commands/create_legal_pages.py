from django.core.management.base import BaseCommand
from django.utils import timezone

from marketing.models import Page


class Command(BaseCommand):
    help = 'Create Privacy Notice and Terms of Use pages'

    def handle(self, *args, **options):
        self._create_privacy_notice()
        self._create_terms_of_use()
        self.stdout.write(self.style.SUCCESS('Legal pages created successfully.'))

    def _create_privacy_notice(self):
        page, created = Page.objects.update_or_create(
            slug='privacy',
            defaults={
                'title': 'Privacy Notice',
                'status': 'published',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'time': 1700000000000,
                                'version': '2.30.2',
                                'blocks': [
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Privacy Notice', 'level': 1}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'Last updated: March 2026'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Introduction', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'BeyondCode AI ("we", "our", "us") is committed to protecting and respecting your privacy. This Privacy Notice explains how we collect, use, disclose, and safeguard your information when you visit our website and use our services.'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Information We Collect', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'We collect information that you provide directly to us when you register for an account, contact us for support, or use our services.'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'How We Use Your Information', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'We use the information we collect to provide and improve our services, communicate with you, and comply with legal obligations.'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Contact Us', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'If you have questions about this Privacy Notice, please contact us at privacy@beyondcode.ai'}
                                    }
                                ]
                            }
                        }
                    ]
                },
                'seo_title': 'Privacy Notice',
                'seo_description': 'Learn how BeyondCode AI collects, uses, and protects your personal information.',
            },
        )
        action = 'created' if created else 'updated'
        self.stdout.write(f'  Privacy Notice page {action}.')

    def _create_terms_of_use(self):
        page, created = Page.objects.update_or_create(
            slug='terms',
            defaults={
                'title': 'Terms of Use',
                'status': 'published',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': {
                                'time': 1700000000000,
                                'version': '2.30.2',
                                'blocks': [
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Terms of Use', 'level': 1}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'Last updated: March 2026'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Acceptance of Terms', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'By accessing and using BeyondCode AI website and services, you accept and agree to be bound by the terms and provision of this agreement.'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Use License', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'Permission is granted to temporarily download one copy of the materials on BeyondCode AI\'s website for personal, non-commercial transitory viewing only.'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Disclaimer', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'The materials on BeyondCode AI\'s website are provided on an \'as is\' basis. BeyondCode AI makes no warranties, expressed or implied.'}
                                    },
                                    {
                                        'type': 'header',
                                        'data': {'text': 'Governing Law', 'level': 2}
                                    },
                                    {
                                        'type': 'paragraph',
                                        'data': {'text': 'These terms and conditions are governed by and construed in accordance with the laws of the jurisdiction in which BeyondCode AI operates.'}
                                    }
                                ]
                            }
                        }
                    ]
                },
                'seo_title': 'Terms of Use',
                'seo_description': 'Terms and conditions for using BeyondCode AI website and services.',
            },
        )
        action = 'created' if created else 'updated'
        self.stdout.write(f'  Terms of Use page {action}.')