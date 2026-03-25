#!/usr/bin/env python
"""
Script to add missing essential pages back to the site:
- About
- Pricing  
- Privacy Notice
- Terms of Use
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from marketing.models import Page

def add_missing_pages():
    """Add the missing essential pages back to the database."""
    
    pages_to_create = [
        {
            'title': 'About',
            'slug': 'about',
            'status': 'published',
            'seo_title': 'About Us - BeyondCode AI',
            'seo_description': 'Learn about BeyondCode AI and our mission to transform debt collection with AI-powered automation.',
            'blocks_json': {
                "html": """
                <div class="about-container">

                <section class="about-hero">
                <div class="about-overlay">
                    <h1>About Us</h1>
                    <p>We build powerful digital experiences that help businesses grow.</p>
                </div>
                </section>

                <section class="about-content">
                <div class="row">
                    <div class="col">
                    <h2>Who We Are</h2>
                    <p>
                        We are a passionate team of developers, designers, and strategists dedicated
                        to creating high-quality web solutions.
                    </p>
                    </div>
                    <div class="col">
                    <img src="https://via.placeholder.com/500x300" />
                    </div>
                </div>
                </section>

                <section class="about-mission">
                <div class="row">
                    <div class="col">
                    <h3>Our Mission</h3>
                    <p>To empower businesses through innovative technology.</p>
                    </div>
                    <div class="col">
                    <h3>Our Vision</h3>
                    <p>To become a leading digital solutions provider.</p>
                    </div>
                </div>
                </section>

                <section class="about-team">
                <h2>Our Team</h2>
                <div class="row team-row">
                    <div class="team-card">
                    <img src="https://via.placeholder.com/150" />
                    <h4>John Doe</h4>
                    <p>Frontend Developer</p>
                    </div>
                    <div class="team-card">
                    <img src="https://via.placeholder.com/150" />
                    <h4>Jane Smith</h4>
                    <p>Backend Developer</p>
                    </div>
                </div>
                </section>

                </div>
                """,

                "css": """
                .about-container {
                font-family: Arial, sans-serif;
                color: #333;
                }

                .about-hero {
                background: url('https://via.placeholder.com/1600x500') center/cover no-repeat;
                height: 400px;
                }

                .about-overlay {
                background: rgba(0,0,0,0.6);
                color: #fff;
                height: 100%;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
                }

                .about-content, .about-mission, .about-team {
                padding: 50px 20px;
                }

                .row {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                }

                .col {
                flex: 1;
                min-width: 280px;
                }

                .about-mission {
                background: #f7f7f7;
                text-align: center;
                }

                .about-team {
                text-align: center;
                }

                .team-card {
                width: 200px;
                padding: 20px;
                border: 1px solid #eee;
                border-radius: 10px;
                }

                .team-card img {
                width: 100%;
                border-radius: 50%;
                }
                """
}
        },
        {
            'title': 'Pricing',
            'slug': 'pricing',
            'status': 'published',
            'seo_title': 'Pricing Plans - BeyondCode AI',
            'seo_description': 'Flexible pricing plans for AI-powered debt collection solutions. Choose the plan that fits your needs.',
           'blocks_json': {
                    "html": """
                <section class="pricing-hero">
                <div class="container text-center">
                    <h1>Simple, Transparent Pricing</h1>
                    <p>Choose the plan that fits your needs. No hidden fees.</p>
                </div>
                </section>

                <section class="pricing-section">
                <div class="pricing-grid">

                    <div class="pricing-card">
                    <h3>Starter</h3>
                    <h2>€499/mo</h2>
                    <ul>
                        <li>Up to 1,000 accounts</li>
                        <li>Basic AI outreach</li>
                        <li>Email notifications</li>
                    </ul>
                    <button>Get Started</button>
                    </div>

                    <div class="pricing-card highlight">
                    <h3>Professional</h3>
                    <h2>€1,299/mo</h2>
                    <ul>
                        <li>Up to 5,000 accounts</li>
                        <li>Advanced AI</li>
                        <li>Phone & SMS</li>
                    </ul>
                    <button>Get Started</button>
                    </div>

                    <div class="pricing-card">
                    <h3>Enterprise</h3>
                    <h2>Custom</h2>
                    <ul>
                        <li>Unlimited accounts</li>
                        <li>Custom AI</li>
                        <li>API integration</li>
                    </ul>
                    <button>Contact Sales</button>
                    </div>

                </div>
                </section>
                """,

                    "css": """
                .pricing-hero {
                padding: 60px 20px;
                text-align: center;
                }

                .pricing-section {
                padding: 50px 20px;
                }

                .pricing-grid {
                display: flex;
                gap: 20px;
                flex-wrap: wrap;
                justify-content: center;
                }

                .pricing-card {
                width: 280px;
                padding: 20px;
                border: 1px solid #eee;
                border-radius: 10px;
                text-align: center;
                }

                .pricing-card.highlight {
                background: #333;
                color: #fff;
                }

                .pricing-card button {
                margin-top: 15px;
                padding: 10px;
                width: 100%;
                }
                """
                }
        },
        {
            'title': 'Privacy Notice',
            'slug': 'privacy',
            'status': 'published',
            'seo_title': 'Privacy Notice - BeyondCode AI',
            'seo_description': 'Our commitment to protecting your data and privacy in accordance with GDPR and EU regulations.',
            'blocks_json': {
                    "html": """
                <section class="page-hero">
                <h1>Privacy Notice</h1>
                <p>Your privacy is our priority.</p>
                </section>

                <section class="page-content">
                <div class="content-box">
                    <h2>Data Protection</h2>
                    <p>We comply with GDPR and protect your data.</p>
                </div>

                <div class="content-box">
                    <h2>What We Collect</h2>
                    <p>We collect only necessary data for services.</p>
                </div>

                <div class="content-box">
                    <h2>Your Rights</h2>
                    <p>You can access, update or delete your data.</p>
                </div>
                </section>
                """,

                    "css": """
                .page-hero {
                text-align: center;
                padding: 60px 20px;
                }

                .page-content {
                max-width: 800px;
                margin: auto;
                padding: 40px 20px;
                }

                .content-box {
                margin-bottom: 30px;
                }
                """
                }
        },
        {
            'title': 'Terms of Use',
            'slug': 'terms',
            'status': 'published',
            'seo_title': 'Terms of Use - BeyondCode AI',
            'seo_description': 'Terms and conditions for using BeyondCode AI services and platform.',
            'blocks_json': {
                    "html": """
                <section class="page-hero">
                <h1>Terms of Use</h1>
                <p>Please read carefully before using our services.</p>
                </section>

                <section class="page-content">

                <div class="content-box">
                    <h2>Acceptance of Terms</h2>
                    <p>By using our services, you agree to our terms.</p>
                </div>

                <div class="content-box">
                    <h2>Service Usage</h2>
                    <p>You must use services legally and responsibly.</p>
                </div>

                <div class="content-box">
                    <h2>Intellectual Property</h2>
                    <p>All content is owned and protected by law.</p>
                </div>

                <div class="content-box">
                    <h2>Limitation of Liability</h2>
                    <p>We are not liable for indirect damages.</p>
                </div>

                </section>
                """,

                    "css": """
                .page-hero {
                text-align: center;
                padding: 60px 20px;
                }

                .page-content {
                max-width: 800px;
                margin: auto;
                padding: 40px 20px;
                }

                .content-box {
                margin-bottom: 30px;
                }
                """
                }
        }
    ]
    
    print("Adding missing essential pages...")
    
    for page_data in pages_to_create:
        # Check if page already exists
        page, created = Page.objects.get_or_create(
            slug=page_data['slug'],
            defaults=page_data
        )
        
        if created:
            print(f"✅ Created page: {page.title}")
        else:
            print(f"⚠️  Page already exists: {page.title}")
            # Update existing page with new content
            for field, value in page_data.items():
                setattr(page, field, value)
            page.save()
            print(f"📝 Updated page: {page.title}")
    
    print("\n✅ All essential pages have been added/updated!")
    print("\nPages available:")
    for page in Page.objects.filter(slug__in=['about', 'pricing', 'privacy', 'terms']):
        print(f"- {page.title} ({page.slug}) - Status: {page.status}")

if __name__ == '__main__':
    add_missing_pages()