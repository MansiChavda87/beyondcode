import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from marketing.models import Page

def create_home_page():
    # Check if home page exists
    try:
        home_page = Page.objects.get(slug='home')
        print(f'Home page already exists: {home_page.title}')
        return
    except Page.DoesNotExist:
        print('Creating home page...')

    # Create the home page with the "One Platform for Compliant AI Collections" section
    blocks_json = {
        'blocks': [
            {
                'type': 'feature_grid',
                'title': 'One Platform for Compliant AI Collections',
                'subtitle': 'Unify your outreach, compliance, and analytics in one platform—saving time and cutting costs.',
                'items': [
                    {
                        'icon': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-zap w-5 h-5 text-primary"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path></svg>',
                        'title': 'Automated Outreach at Scale',
                        'body': 'Every debtor on your list gets contacted on time, every cycle. Scale from hundreds to thousands of calls without adding headcount.'
                    },
                    {
                        'icon': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield w-5 h-5 text-primary-foreground"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path></svg>',
                        'title': 'GDPR-Compliant by Design',
                        'body': 'Calling windows, retry rules, and consent guardrails enforced automatically. Audit-ready evidence logs for every interaction.'
                    },
                    {
                        'icon': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chart-column w-5 h-5 text-primary"><path d="M3 3v16a2 2 0 0 0 2 2h16"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path></svg>',
                        'title': 'Predictable Recovery Operations',
                        'body': 'Turn collections into measurable weekly output with real-time analytics, coverage reports, and structured outcome tracking.'
                    }
                ]
            }
        ]
    }

    page = Page.objects.create(
        title='Home',
        slug='home',
        status='published',
        blocks_json=blocks_json,
        seo_title='BeyondCode AI - AI-Powered Debt Collection for EU Lenders',
        seo_description='Transform your debt collection operations with AI-powered automation while maintaining full EU compliance. Scale your collections without adding headcount.'
    )

    print(f'Created home page: {page.title}')

if __name__ == '__main__':
    create_home_page()