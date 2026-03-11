from django.core.management.base import BaseCommand
from django.utils import timezone

from marketing.models import Page, Post, NavMenu, Footer, Category, Tag


class Command(BaseCommand):
    help = 'Seed sample CMS content: pages, blog posts, navigation, and footer'

    def handle(self, *args, **options):
        self._seed_categories_tags()
        self._seed_pages()
        self._seed_posts()
        self._seed_navigation()
        self._seed_footer()
        self.stdout.write(self.style.SUCCESS('CMS content seeded successfully.'))

    # -- Categories & Tags --------------------------------------------------

    def _seed_categories_tags(self):
        for name, slug in [
            ('Business Tools', 'business-tools'),
            ('Project Management', 'project-management'),
            ('Compliance', 'compliance'),
            ('Product Updates', 'product-updates'),
        ]:
            Category.objects.get_or_create(slug=slug, defaults={'name': name})

        for name, slug in [
            ('AI', 'ai'),
            ('Automation', 'automation'),
            ('DMS', 'dms'),
            ('Enterprise', 'enterprise'),
            ('Security', 'security'),
            ('Workflows', 'workflows'),
        ]:
            Tag.objects.get_or_create(slug=slug, defaults={'name': name})
        self.stdout.write('  Categories & tags created.')

    # -- Pages --------------------------------------------------------------

    def _seed_pages(self):
        pages = [
            {
                'title': 'Privacy Notice',
                'slug': 'privacy',
                'status': 'published',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'header', 'data': {'text': 'Privacy Notice', 'level': 1}},
                                {'type': 'paragraph', 'data': {'text': 'Last updated: March 2026'}},
                                {'type': 'header', 'data': {'text': 'Introduction', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'BeyondCode AI ("we", "our", "us") is committed to protecting and respecting your privacy. This Privacy Notice explains how we collect, use, disclose, and safeguard your information when you visit our website and use our services.'}},
                                {'type': 'header', 'data': {'text': 'Information We Collect', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'We collect information that you provide directly to us when you:'}},
                                {'type': 'list', 'data': {'style': 'unordered', 'items': [
                                    'Register for an account or use our services',
                                    'Contact us for customer support or sales inquiries',
                                    'Subscribe to our newsletter or marketing communications',
                                    'Participate in surveys, contests, or promotions',
                                    'Provide feedback or communicate with us through various channels'
                                ]}},
                                {'type': 'header', 'data': {'text': 'How We Use Your Information', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'We use the information we collect for various purposes, including:'}},
                                {'type': 'list', 'data': {'style': 'unordered', 'items': [
                                    'Providing, maintaining, and improving our services',
                                    'Processing transactions and sending related communications',
                                    'Sending you technical notices, updates, security alerts, and support messages',
                                    'Communicating with you about products, services, offers, and events',
                                    'Monitoring and analyzing trends, usage, and activities',
                                    'Detecting, investigating, and preventing fraudulent or illegal activities'
                                ]}},
                                {'type': 'header', 'data': {'text': 'Information Sharing and Disclosure', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'We may share your information with third parties in the following circumstances:'}},
                                {'type': 'list', 'data': {'style': 'unordered', 'items': [
                                    'With vendors, consultants, and other service providers who need access to your information to carry out work on our behalf',
                                    'In connection with, or during negotiations of, any merger, sale of company assets, financing, or acquisition of all or a portion of our business',
                                    'With your consent or at your direction',
                                    'To comply with legal obligations, enforce our policies, or protect our rights, privacy, safety, or property'
                                ]}},
                                {'type': 'header', 'data': {'text': 'Data Retention', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'We will retain your information only for as long as is necessary for the purposes set out in this Privacy Notice. We will retain and use your information to the extent necessary to comply with our legal obligations, resolve disputes, and enforce our policies.'}},
                                {'type': 'header', 'data': {'text': 'Your Rights and Choices', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Depending on your location, you may have certain rights regarding your personal information, including:'}},
                                {'type': 'list', 'data': {'style': 'unordered', 'items': [
                                    'Access to your personal information',
                                    'Correction of inaccurate personal information',
                                    'Deletion of your personal information',
                                    'Restriction of processing your personal information',
                                    'Objection to processing your personal information',
                                    'Data portability'
                                ]}},
                                {'type': 'header', 'data': {'text': 'Contact Us', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'If you have questions or comments about this Privacy Notice, please contact us at:'}},
                                {'type': 'paragraph', 'data': {'text': 'Email: privacy@beyondcode.ai<br>Address: BeyondCode AI, Data Protection Officer, [Company Address]'}},
                            ])},
                        },
                        {
                            'type': 'callout',
                            'title': 'EU Data Protection',
                            'body': 'We comply with the General Data Protection Regulation (GDPR) and other applicable EU data protection laws.',
                        },
                    ]
                },
                'seo_title': 'Privacy Notice',
                'seo_description': 'Learn how BeyondCode AI collects, uses, and protects your personal information.',
            },
            {
                'title': 'Terms of Use',
                'slug': 'terms',
                'status': 'published',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'header', 'data': {'text': 'Terms of Use', 'level': 1}},
                                {'type': 'paragraph', 'data': {'text': 'Last updated: March 2026'}},
                                {'type': 'header', 'data': {'text': 'Acceptance of Terms', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'By accessing and using BeyondCode AI ("we", "our", "us") website and services, you accept and agree to be bound by the terms and provision of this agreement. In addition, when using our services, you shall be subject to any posted guidelines or rules applicable to such services.'}},
                                {'type': 'header', 'data': {'text': 'Use License', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Permission is granted to temporarily download one copy of the materials (information or software) on BeyondCode AI\'s website for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:'}},
                                {'type': 'list', 'data': {'style': 'unordered', 'items': [
                                    'Modify or copy the materials',
                                    'Use the materials for any commercial purpose or for any public display (commercial or non-commercial)',
                                    'Attempt to decompile or reverse engineer any software contained on the site',
                                    'Remove any copyright or other proprietary notations from the materials',
                                    'Transfer the materials to another person or "mirror" the materials on any other server'
                                ]}},
                                {'type': 'header', 'data': {'text': 'Disclaimer', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'The materials on BeyondCode AI\'s website are provided on an \'as is\' basis. BeyondCode AI makes no warranties, expressed or implied, and hereby disclaims and negates all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.'}},
                                {'type': 'header', 'data': {'text': 'Limitations', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'In no event shall BeyondCode AI or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on BeyondCode AI\'s website, even if BeyondCode AI or a BeyondCode AI authorized representative has been notified orally or in writing of the possibility of such damage.'}},
                                {'type': 'header', 'data': {'text': 'Accuracy of Materials', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'The materials appearing on BeyondCode AI\'s website could include technical, typographical, or photographic errors. BeyondCode AI does not warrant that any of the materials on its website are accurate, complete, or current. BeyondCode AI may make changes to the materials contained on its website at any time without notice.'}},
                                {'type': 'header', 'data': {'text': 'Links', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'BeyondCode AI has not reviewed all of the sites linked to our website and is not responsible for the contents of any such linked site. The inclusion of any link does not imply endorsement by BeyondCode AI of the site. Use of any such linked website is at the user\'s own risk.'}},
                                {'type': 'header', 'data': {'text': 'Modifications', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'BeyondCode AI may revise these terms of service for its website at any time without notice. By using this website you are agreeing to be bound by the then current version of these terms of service.'}},
                                {'type': 'header', 'data': {'text': 'Governing Law', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'These terms and conditions are governed by and construed in accordance with the laws of the jurisdiction in which BeyondCode AI operates and you irrevocably submit to the exclusive jurisdiction of the courts in that state or location.'}},
                            ])},
                        },
                        {
                            'type': 'callout',
                            'title': 'Professional Services',
                            'body': 'Our services are intended for professional use by businesses and organizations. Individual consumers should consult with their legal advisors regarding compliance requirements.',
                        },
                    ]
                },
                'seo_title': 'Terms of Use',
                'seo_description': 'Terms and conditions for using BeyondCode AI website and services.',
            },
            {
                'title': 'About BeyondCode AI',
                'slug': 'about',
                'status': 'published',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'header', 'data': {'text': 'Our Mission', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'BeyondCode AI was founded to transform debt collection for EU-regulated lenders. We build AI-powered tools that automate outreach while maintaining full compliance.'}},
                                {'type': 'paragraph', 'data': {'text': 'Our platform combines automated calling, intelligent scripts, and audit-ready evidence logs to help lenders recover funds efficiently and ethically.'}},
                                {'type': 'header', 'data': {'text': 'Our Story', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'We started with firsthand experience in the collections industry. We saw the inefficiencies, compliance challenges, and manual work that plagued traditional approaches. We set out to build the platform we always wished we had.'}},
                            ])},
                        },
                        {
                            'type': 'callout',
                            'title': 'Trusted by EU Lenders',
                            'body': 'From fintech startups to established financial institutions, we power collections operations across Europe.',
                        },
                        {
                            'type': 'feature_grid',
                            'items': [
                                {'title': 'AI-Powered Outreach', 'body': 'Every debtor on your list gets contacted on time, every cycle. Scale from hundreds to thousands of calls without adding headcount.'},
                                {'title': 'GDPR-Compliant by Design', 'body': 'Calling windows, retry rules, and consent guardrails enforced automatically. Audit-ready evidence logs for every interaction.'},
                                {'title': 'Predictable Operations', 'body': 'Turn collections into measurable weekly output with real-time analytics, coverage reports, and structured outcome tracking.'},
                                {'title': 'Zero Manual Work', 'body': 'Free your team from repetitive chasing. Humans only for exceptions and disputes.'},
                            ],
                        },
                        {
                            'type': 'cta',
                            'title': 'Ready to transform your collections?',
                            'body': 'See the product in action with a personalized demo from our team.',
                            'button_label': 'Book a Demo',
                            'button_url': '/contact/',
                        },
                    ]
                },
                'seo_title': 'About BeyondCode AI',
                'seo_description': 'Learn how BeyondCode AI helps EU lenders automate collections while maintaining compliance.',
            },
            {
                'title': 'Contact Us',
                'slug': 'contact',
                'status': 'published',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'header', 'data': {'text': 'Get in Touch', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Have questions? Want to see a demo? Our team typically responds within one business day.'}},
                                {'type': 'paragraph', 'data': {'text': 'Email us at hello@beyondcode.ai or use the form below. For enterprise inquiries, reach out to sales@beyondcode.ai.'}},
                            ]),
                        },
                        {
                            'type': 'callout',
                            'title': 'Enterprise & EU Compliance',
                            'body': 'For organizations with 100+ accounts, dedicated onboarding, or specific compliance requirements, contact our enterprise team directly at enterprise@beyondcode.ai.',
                        },
                    ]
                },
                'seo_title': 'Contact Us — Get a Demo',
                'seo_description': 'Contact the team for demos, support, and enterprise inquiries.',
            },
            {
                'title': 'Pricing',
                'slug': 'pricing',
                'status': 'published',
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'header', 'data': {'text': 'Simple, transparent pricing', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'No hidden fees. No long-term contracts. Start with a free trial and scale as you grow.'}},
                            ]),
                        },
                        {
                            'type': 'pricing_table',
                            'plans': [
                                {
                                    'title': 'Starter',
                                    'price': '€49/mo',
                                    'features': ['Up to 500 accounts', '1 workspace', 'Basic AI outreach', 'Email support'],
                                },
                                {
                                    'title': 'Professional',
                                    'price': '€199/mo',
                                    'features': ['Unlimited accounts', '5 workspaces', 'Advanced AI + compliance', 'Priority support', 'Custom scripts'],
                                },
                                {
                                    'title': 'Enterprise',
                                    'price': 'Custom',
                                    'features': ['Unlimited everything', 'SSO & compliance', 'Dedicated CSM', 'SLA guarantees', 'Custom integrations'],
                                },
                            ],
                        },
                        {
                            'type': 'faq',
                            'items': [
                                {'question': 'Can I switch plans anytime?', 'answer': 'Yes. Upgrade or downgrade at any time. Changes take effect on your next billing cycle.'},
                                {'question': 'Is there a free trial?', 'answer': 'Absolutely. Every plan includes a 14-day free trial with full feature access. No credit card required.'},
                                {'question': 'What payment methods do you accept?', 'answer': 'We accept all major credit cards and bank transfers. Enterprise customers can pay by invoice with NET-30 terms.'},
                                {'question': 'Do you offer discounts for non-profits?', 'answer': 'Yes, we offer 30% off for registered non-profit organizations. Contact us at hello@beyondcode.ai for details.'},
                            ],
                        },
                        {
                            'type': 'cta',
                            'title': 'Not sure which plan is right for you?',
                            'body': 'Our team can help you find the perfect fit for your collections operation.',
                            'button_label': 'Talk to Sales',
                            'button_url': '/contact/',
                        },
                    ]
                },
                'seo_title': 'Pricing',
                'seo_description': 'Explore plans and pricing. Start free, scale as you grow.',
            },
        ]

        for data in pages:
            page, created = Page.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'status': data['status'],
                    'body_json': None,
                    'blocks_json': data['blocks_json'],
                    'seo_title': data.get('seo_title', ''),
                    'seo_description': data.get('seo_description', ''),
                },
            )
            action = 'created' if created else 'updated'
            self.stdout.write(f'  Page "{page.title}" {action}.')

    # -- Blog Posts ---------------------------------------------------------

    def _seed_posts(self):
        now = timezone.now()
        cat_legaltech = Category.objects.filter(slug='business-tools').first()
        cat_clm = Category.objects.filter(slug='project-management').first()
        cat_compliance = Category.objects.filter(slug='compliance').first()

        tag_ai = Tag.objects.filter(slug='ai').first()
        tag_automation = Tag.objects.filter(slug='automation').first()
        tag_clm = Tag.objects.filter(slug='dms').first()
        tag_enterprise = Tag.objects.filter(slug='enterprise').first()
        tag_security = Tag.objects.filter(slug='security').first()
        tag_workflows = Tag.objects.filter(slug='workflows').first()

        posts_data = [
            {
                'title': 'How AI Is Transforming Debt Collections in 2026',
                'slug': 'ai-debt-collections-2026',
                'status': 'published',
                'author_name': 'Sarah Chen',
                'excerpt': 'AI-powered debt collection has finally crossed the accuracy threshold that makes fully automated outreach viable for EU-regulated lenders.',
                'publish_at': now - timezone.timedelta(days=5),
                'categories': [cat_legaltech, cat_clm],
                'tags': [tag_ai, tag_clm],
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'paragraph', 'data': {'text': 'The collections industry has talked about AI-powered outreach for years, but 2026 marks a genuine inflection point. Accuracy rates for debtor identification and compliance checks have crossed 95%, making these tools reliable enough for production use without human double-checking on every call.'}},
                                {'type': 'header', 'data': {'text': 'What Changed?', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Three converging trends made this possible: domain-specific fine-tuning of large language models on millions of real debtor interactions, retrieval-augmented generation (RAG) that grounds AI outputs in your organization\'s own compliance playbook, and better calibration techniques that make models say "I don\'t know" instead of hallucinating.'}},
                                {'type': 'header', 'data': {'text': 'Practical Impact', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Teams using AI outreach report 60-80% reductions in first-pass contact time. For high-volume operations processing hundreds of debtor accounts each month, this translates to millions in saved outsourcing spend.'}},
                                {'type': 'header', 'data': {'text': 'What to Look For', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'When evaluating AI debt collection tools, focus on: accuracy metrics on your specific debtor types, the ability to train on your compliance playbook and preferred scripts, integration with your existing workflow and debtor management systems, and transparent audit trails that show exactly why the AI made each decision.'}},
                            ]),
                        },
                        {
                            'type': 'comparison_table',
                            'headers': ['Capability', 'Traditional Collections', 'AI-Assisted Collections'],
                            'rows': [
                                ['Debtor first-pass contact', '45 minutes', '3 minutes'],
                                ['Compliance identification', 'Manual checklist', 'Automated + scored'],
                                ['Script adherence', 'Memory-dependent', 'Systematically enforced'],
                                ['Volume capacity', '5-10 accounts/day', '100+ accounts/day'],
                            ],
                        },
                        {
                            'type': 'cta',
                            'title': 'See AI debt collection in action',
                            'body': 'Upload a sample debtor list and get an instant outreach analysis.',
                            'button_label': 'Try It Free',
                            'button_url': '/contact/',
                        },
                    ]
                },
            },
            {
                'title': '5 Workflow Automations Every Collections Team Should Deploy',
                'slug': 'collections-workflow-automations',
                'status': 'published',
                'author_name': 'Marcus Wright',
                'excerpt': 'Stop reinventing the wheel. These five workflow automations will save your team hours every week with minimal setup effort.',
                'publish_at': now - timezone.timedelta(days=12),
                'categories': [cat_clm],
                'tags': [tag_automation, tag_workflows, tag_clm],
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'paragraph', 'data': {'text': 'Most collections teams know they should automate more, but choosing where to start is paralyzing. After working with hundreds of EU lenders, we\'ve identified the five automations that deliver the highest ROI with the least implementation effort.'}},
                                {'type': 'header', 'data': {'text': '1. Automated Outreach Scheduling', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Auto-dialer schedules and retry rules based on debtor behavior and compliance windows. Set up automated alerts 90, 60, and 30 days before any payment due date. Link these to your calendar and team chat so the right stakeholder gets notified at the right time.'}},
                                {'type': 'header', 'data': {'text': '2. Compliance Routing', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Route debtor interactions for compliance review based on risk level, amount, and debtor type. Low-risk accounts go straight to automated outreach. Medium-risk triggers manager review. High-risk adds compliance and legal sign-off. No more email chains asking "who needs to approve this?"'}},
                                {'type': 'header', 'data': {'text': '3. Script Selection', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'When a team member needs to contact a debtor, a short intake form should automatically select the right script, pre-fill known data from your CRM, and route it to the correct workflow. This alone eliminates 70% of "can you send me the right script?" requests.'}},
                                {'type': 'header', 'data': {'text': '4. Obligation Tracking', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Extract key obligations from debtor agreements and create automated tasks with deadlines. Payment milestones, contact requirements, reporting obligations — these should all flow into a central tracker with automated reminders.'}},
                                {'type': 'header', 'data': {'text': '5. Expiration & Compliance Alerts', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Certificates of insurance, regulatory filings, debtor agreements — all have expiration dates. Automate monitoring and alert the responsible party well before deadlines hit.'}},
                            ]),
                        },
                        {
                            'type': 'feature_grid',
                            'items': [
                                {'title': 'Automated Outreach', 'body': 'Never miss a debtor contact or compliance window again.'},
                                {'title': 'Compliance Routing', 'body': 'Route interactions to the right approvers automatically.'},
                                {'title': 'Script Selection', 'body': 'Auto-select and pre-fill the right script for each debtor.'},
                                {'title': 'Obligation Tracking', 'body': 'Extract and track obligations from debtor agreements.'},
                            ],
                        },
                        {
                            'type': 'callout',
                            'title': 'Start Small',
                            'body': 'You don\'t need to automate everything at once. Pick the one automation that addresses your biggest pain point and build from there.',
                        },
                    ]
                },
            },
            {
                'title': 'Building a Compliance-First Culture in Collections',
                'slug': 'compliance-first-collections',
                'status': 'published',
                'author_name': 'Priya Nair',
                'excerpt': 'Compliance isn\'t just about checking boxes. Here\'s how forward-thinking collections teams are embedding compliance into their daily workflows.',
                'publish_at': now - timezone.timedelta(days=20),
                'categories': [cat_compliance],
                'tags': [tag_enterprise, tag_security, tag_workflows],
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'paragraph', 'data': {'text': 'Regulatory landscapes are getting more complex every year. GDPR, PSD2, local consumer protection laws — teams can\'t afford to treat compliance as an annual audit exercise. It needs to be woven into everyday operations.'}},
                                {'type': 'header', 'data': {'text': 'From Reactive to Proactive', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'The traditional model is reactive: something goes wrong, the team investigates, policies get updated. A compliance-first culture flips this by building guardrails into processes before issues arise.'}},
                                {'type': 'header', 'data': {'text': 'Key Principles', 'level': 2}},
                                {'type': 'list', 'data': {'style': 'unordered', 'items': ['Make the compliant path the easiest path', 'Automate compliance checks at the point of action', 'Provide real-time feedback, not after-the-fact audits', 'Invest in training that\'s contextual, not annual slide decks']}},
                                {'type': 'header', 'data': {'text': 'Technology\'s Role', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Modern collections platforms can enforce compliance automatically: required fields that can\'t be skipped, prohibited terms that trigger warnings, mandatory approval workflows for high-risk debtor interactions, and automated regulatory reporting.'}},
                            ]),
                        },
                        {
                            'type': 'quote',
                            'quote': 'The best compliance program is one where people don\'t even realize they\'re being compliant — because the systems make it effortless.',
                             'author': 'Collections Compliance Expert',
                        },
                        {
                            'type': 'faq',
                            'items': [
                                {'question': 'How do I get buy-in from leadership for compliance tooling?', 'answer': 'Frame it in terms of risk reduction and cost avoidance. A single compliance violation can cost more than years of tooling investment. Quantify your current exposure.'},
                                {'question': 'Should compliance be centralized or distributed?', 'answer': 'The answer is both. Set centralized policies and standards, but embed compliance champions and automated checks into each business unit\'s workflow.'},
                                {'question': 'How often should compliance policies be reviewed?', 'answer': 'At minimum quarterly, but the real answer is continuously. Regulatory changes should trigger immediate policy reviews in affected areas.'},
                            ],
                        },
                    ]
                },
            },
            {
                'title': 'Product Roadmap: What\'s Coming Next',
                'slug': 'product-roadmap-2026',
                'status': 'published',
                'author_name': 'Team',
                'excerpt': 'A look at the features and improvements shipping in the next two quarters, including enhanced AI capabilities and new integrations.',
                'publish_at': now - timezone.timedelta(days=2),
                'categories': [Category.objects.filter(slug='product-updates').first()],
                'tags': [tag_ai, tag_automation, tag_enterprise],
                'blocks_json': {
                    'blocks': [
                        {
                            'type': 'rich_text',
                            'content': _editorjs_body([
                                {'type': 'paragraph', 'data': {'text': 'We\'ve been heads-down building, and we\'re excited to share what\'s coming next. These updates are driven directly by feedback from our customers and our vision for where the product is headed.'}},
                                {'type': 'header', 'data': {'text': 'Q1 2026: Intelligence Layer', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'Our new intelligence layer brings AI-powered insights to every part of the platform. Debtor risk scores, script recommendations based on your history, and predictive analytics for collection cycle times.'}},
                                {'type': 'header', 'data': {'text': 'Q2 2026: Integration Ecosystem', 'level': 2}},
                                {'type': 'paragraph', 'data': {'text': 'We\'re launching new integrations with popular tools, plus an API gateway that makes it trivial to connect the product to any system in your stack.'}},
                            ]),
                        },
                        {
                            'type': 'feature_grid',
                            'items': [
                                {'title': 'AI Risk Scoring', 'body': 'Automatic risk scores for every debtor based on interaction analysis and historical data.'},
                                {'title': 'Script Library', 'body': 'A searchable library of approved scripts with AI-powered recommendations.'},
                                 {'title': 'CRM Integration', 'body': 'Native bi-directional sync with your CRM.'},
                                 {'title': 'API Gateway', 'body': 'Connect the product to any system with a developer-friendly API.'},
                            ],
                        },
                        {
                            'type': 'cta',
                            'title': 'Want early access?',
                            'body': 'Join our beta program to test new features before they launch.',
                            'button_label': 'Join the Beta',
                            'button_url': '/contact/',
                        },
                    ]
                },
            },
        ]

        for data in posts_data:
            categories = data.pop('categories', [])
            tags = data.pop('tags', [])
            post, created = Post.objects.update_or_create(
                slug=data['slug'],
                defaults={
                    'title': data['title'],
                    'status': data['status'],
                    'author_name': data['author_name'],
                    'excerpt': data['excerpt'],
                    'publish_at': data.get('publish_at'),
                    'body_json': None,
                    'blocks_json': data['blocks_json'],
                },
            )
            post.categories.set([c for c in categories if c])
            post.tags.set([t for t in tags if t])
            action = 'created' if created else 'updated'
            self.stdout.write(f'  Post "{post.title}" {action}.')

    # -- Navigation ---------------------------------------------------------

    def _seed_navigation(self):
        nav, _ = NavMenu.objects.update_or_create(
            name='Primary',
            defaults={
                'items_json': [
                    {'label': 'About', 'url': '/about/'},
                    {'label': 'Pricing', 'url': '/pricing/'},
                    {'label': 'Blog', 'url': '/blog/'},
                    {'label': 'Contact', 'url': '/contact/'},
                ],
            },
        )
        self.stdout.write(f'  Navigation menu seeded.')

    # -- Footer -------------------------------------------------------------

    def _seed_footer(self):
        footer, _ = Footer.objects.update_or_create(
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
        self.stdout.write(f'  Footer seeded.')


# -- Helpers ----------------------------------------------------------------

def _editorjs_body(blocks):
    """Wrap a list of EditorJS block dicts in the standard EditorJS envelope."""
    return {
        'time': 1700000000000,
        'version': '2.30.2',
        'blocks': blocks,
    }