#!/usr/bin/env python3
"""
Script to update the Demo Page with new sections using GrapesJS content
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'beyondcode_project'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beyondcode_project.settings')
django.setup()

from marketing.models import Page


def update_demo_page_with_sections():
    """Update the demo page with all requested sections"""
    print("Updating Demo Page with new sections...")
    
    # Complete content with all sections from the reference file
    complete_content = {
        "html": """
        <main class="min-h-screen bg-background text-foreground overflow-x-hidden">
            <!-- Hero Section -->
            <section class="relative overflow-hidden">
               
                <div class="relative z-10 text-center px-6 pt-8 pb-6 md:pt-12 md:pb-8 max-w-4xl mx-auto">
                    <div class="inline-flex items-center gap-2 px-4 py-1.5 bg-accent text-accent-foreground text-sm font-medium rounded-full mb-8">
                        <span class="w-2 h-2 rounded-full bg-primary"></span>AI-Powered Debt Collection Platform
                    </div>
                    <h1 class="text-4xl md:text-5xl lg:text-6xl font-bold leading-[1.1] mb-6 text-foreground tracking-tight">Bring Your <span class="text-primary">Money Home</span></h1>
                    <p class="text-muted-foreground text-lg md:text-xl max-w-2xl mx-auto mb-10 leading-relaxed">Automate debtor outreach across active portfolios so every account is contacted on time—without growing your team or losing compliance control.</p>
                    <div class="flex flex-col sm:flex-row items-center justify-center gap-4 mb-6">
                        <button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 hover:shadow-lg h-11 bg-primary text-primary-foreground hover:bg-primary/90 px-8 py-6 text-base font-semibold shadow-lg shadow-primary/20">Book a Quick Demo<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-arrow-right w-5 h-5 ml-2"><path d="M5 12h14"></path><path d="m12 5 7 7-7 7"></path></svg></button>
                        <button class="inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg font-semibold ring-offset-background transition-all duration-300 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 border bg-transparent hover:border-primary/50 h-11 px-8 py-6 text-base border-border text-foreground hover:bg-secondary">See How It Works</button>
                    </div>
                    <div class="py-6">
                        <p class="text-center text-muted-foreground text-sm font-medium tracking-wide uppercase mb-6">Trusted by EU-regulated financial institutions</p>
                        <div class="flex flex-wrap items-center justify-center gap-x-10 gap-y-4 px-6">
                            <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BONDORA</span>
                            <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">RAHA24</span>
                            <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BB-FINANCE</span>
                            <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">HYBA FINANCE</span>
                            <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">THEMIS LAW BUREAU</span>
                            <span class="text-muted-foreground/60 font-bold text-sm tracking-widest uppercase">BALTASAR LEASING</span>
                        </div>
                    </div>
                </div>
            </section>

            <!-- One Platform for Compliant AI Collections Section -->
            <section class="section-padding bg-background">
                <div class="max-w-6xl mx-auto px-6">
                    <div class="text-center mb-8">
                        <h2 class="text-3xl md:text-4xl font-bold text-foreground mb-4">One Platform for Compliant AI Collections</h2>
                        <p class="text-muted-foreground text-lg max-w-2xl mx-auto">Unify your outreach, compliance, and analytics in one platform—saving time and cutting costs.</p>
                    </div>
                    <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                            <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-zap w-5 h-5 text-primary"><path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z"></path></svg>
                            </div>
                            <h3 class="text-lg font-bold mb-2">Automated Outreach at Scale</h3>
                            <p class="text-sm leading-relaxed text-muted-foreground">Every debtor on your list gets contacted on time, every cycle. Scale from hundreds to thousands of calls without adding headcount.</p>
                        </div>
                        <div class="rounded-xl p-7 border transition-all bg-primary text-primary-foreground border-primary shadow-lg">
                            <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-primary-foreground/20">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield w-5 h-5 text-primary-foreground"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path></svg>
                            </div>
                            <h3 class="text-lg font-bold mb-2">GDPR-Compliant by Design</h3>
                            <p class="text-sm leading-relaxed text-primary-foreground/80">Calling windows, retry rules, and consent guardrails enforced automatically. Audit-ready evidence logs for every interaction.</p>
                        </div>
                        <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                            <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-chart-column w-5 h-5 text-primary"><path d="M3 3v16a2 2 0 0 0 2 2h16"></path><path d="M18 17V9"></path><path d="M13 17V5"></path><path d="M8 17v-3"></path></svg>
                            </div>
                            <h3 class="text-lg font-bold mb-2">Predictable Recovery Operations</h3>
                            <p class="text-sm leading-relaxed text-muted-foreground">Turn collections into measurable weekly output with real-time analytics, coverage reports, and structured outcome tracking.</p>
                        </div>
                        <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                            <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-brain w-5 h-5 text-primary"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"></path><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"></path><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"></path><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"></path><path d="M6.401 6.5a3 3 0 0 1-.399-1.375"></path></svg>
                            </div>
                            <h3 class="text-lg font-bold mb-2">Intelligent Conversation AI</h3>
                            <p class="text-sm leading-relaxed text-muted-foreground">Natural language processing understands debtor responses, adapts conversation flow, and handles objections intelligently.</p>
                        </div>
                        <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                            <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-clock w-5 h-5 text-primary"><circle cx="12" cy="12" r="10"></circle><polyline points="12,6 12,12 16,14"></polyline></svg>
                            </div>
                            <h3 class="text-lg font-bold mb-2">24/7 Automated Operations</h3>
                            <p class="text-sm leading-relaxed text-muted-foreground">Round-the-clock collection efforts across multiple time zones and languages, ensuring no opportunity is missed.</p>
                        </div>
                        <div class="rounded-xl p-7 border transition-all bg-card text-card-foreground border-border hover:border-primary/30 hover:shadow-md">
                            <div class="w-11 h-11 rounded-lg flex items-center justify-center mb-5 bg-accent">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-file-text w-5 h-5 text-primary"><path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z"></path><polyline points="14,2 14,8 20,8"></polyline><line x1="16" x2="8" y1="13" y2="13"></line><line x1="16" x2="8" y1="17" y2="17"></line><line x1="10" x2="8" y1="9" y2="9"></line></svg>
                            </div>
                            <h3 class="text-lg font-bold mb-2">Complete Audit Trail</h3>
                            <p class="text-sm leading-relaxed text-muted-foreground">Every interaction logged with timestamps, audio recordings, and compliance metadata for regulatory requirements.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Real Results From a Live Portfolio Section -->
            <section class="section-padding bg-secondary/50">
                <div class="max-w-6xl mx-auto px-6">
                    <div class="text-center mb-8">
                        <span class="inline-flex items-center gap-2 px-4 py-1.5 bg-accent text-accent-foreground text-sm font-medium rounded-full mb-6">Case Study · 1 Month Results</span>
                        <h2 class="text-3xl md:text-4xl font-bold text-foreground mb-4">Real Results From a Live Portfolio</h2>
                        <p class="text-muted-foreground text-lg max-w-xl mx-auto">Measurable impact from a single month of automated AI collection on an EU-regulated portfolio.</p>
                    </div>
                    <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">4,000</div>
                            <div class="text-muted-foreground text-xs font-medium">AI Calls Completed</div>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">€20,000</div>
                            <div class="text-muted-foreground text-xs font-medium">In Promised Payments</div>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">150</div>
                            <div class="text-muted-foreground text-xs font-medium">Debtors Reached</div>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">87</div>
                            <div class="text-muted-foreground text-xs font-medium">Hours Saved</div>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">0</div>
                            <div class="text-muted-foreground text-xs font-medium">Manual Work Required</div>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">98%</div>
                            <div class="text-muted-foreground text-xs font-medium">Contact Success Rate</div>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">45,000</div>
                            <div class="text-muted-foreground text-xs font-medium">Portfolio Value Recovered</div>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 text-center hover:shadow-md transition-shadow">
                            <div class="text-2xl md:text-3xl font-bold text-foreground mb-1">15</div>
                            <div class="text-muted-foreground text-xs font-medium">Days Average Collection Time</div>
                        </div>
                    </div>
                    <div class="mt-10 text-center">
                        <a href="https://calendly.com/henri-beyondcode/ai-collections-demo" target="_blank">
                            <button class="inline-flex items-center justify-center gap-2 bg-primary text-primary-foreground hover:bg-primary/90 font-semibold px-10 py-4 rounded-lg text-base transition-all duration-300 shadow-lg hover:shadow-xl">See If It Fits</button>
                        </a>
                    </div>
                </div>
            </section>

            <!-- Transform Your Debt Collection Section -->
            <section class="section-padding bg-background">
                <div class="max-w-6xl mx-auto px-6">
                    <div class="text-center mb-8">
                        <h2 class="text-3xl md:text-4xl font-bold text-foreground mb-4">Transform Your Debt Collection With Our Compliant AI Solution</h2>
                        <p class="text-muted-foreground text-lg max-w-2xl mx-auto">Everything you need to automate, scale, and audit your collection operations—in one platform.</p>
                    </div>
                    <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-5">
                        <div class="bg-card rounded-xl border border-border p-6 hover:border-primary/30 hover:shadow-md transition-all">
                            <h3 class="font-bold text-foreground mb-2">GDPR-Compliant Calling</h3>
                            <p class="text-muted-foreground text-sm">Automated enforcement of calling windows, consent rules, and data retention policies.</p>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 hover:border-primary/30 hover:shadow-md transition-all">
                            <h3 class="font-bold text-foreground mb-2">Personalized Scripts & Tone</h3>
                            <p class="text-muted-foreground text-sm">Tailored conversation flows per debtor profile, segment, and debt stage.</p>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 hover:border-primary/30 hover:shadow-md transition-all">
                            <h3 class="font-bold text-foreground mb-2">Automated Conversations</h3>
                            <p class="text-muted-foreground text-sm">Identity verification, debt notification, and payment agreement—handled automatically.</p>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6 hover:border-primary/30 hover:shadow-md transition-all">
                            <h3 class="font-bold text-foreground mb-2">Zero Manual Dialing</h3>
                            <p class="text-muted-foreground text-sm">Free your team from repetitive chasing. Humans only for exceptions and disputes.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- How It Works Section -->
            <section id="how-it-works" class="section-padding bg-secondary/50">
                <div class="max-w-6xl mx-auto px-6">
                    <div class="text-center mb-8">
                        <h2 class="text-3xl md:text-4xl font-bold text-foreground mb-4">How It Works</h2>
                        <p class="text-muted-foreground text-lg max-w-2xl mx-auto">Four structured steps from onboarding to go-live. Built for fast deployment and clear operational readiness.</p>
                    </div>
                    <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                        <div class="bg-card rounded-xl border border-border p-6">
                            <div class="text-primary font-bold text-lg mb-2">01</div>
                            <h3 class="font-bold text-foreground mb-2">Launch Sprint</h3>
                            <p class="text-muted-foreground text-sm">One guided setup window — live before we end. Accounts + billing ready in days, not months.</p>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6">
                            <div class="text-primary font-bold text-lg mb-2">02</div>
                            <h3 class="font-bold text-foreground mb-2">Telecom Clearance</h3>
                            <p class="text-muted-foreground text-sm">Telephony KYC fast-track with country checklist, path, and next actions. No bureaucratic delays.</p>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6">
                            <div class="text-primary font-bold text-lg mb-2">03</div>
                            <h3 class="font-bold text-foreground mb-2">System Alignment</h3>
                            <p class="text-muted-foreground text-sm">Inputs → decisions → outputs. We map the data flow and connect in phases.</p>
                        </div>
                        <div class="bg-card rounded-xl border border-border p-6">
                            <div class="text-primary font-bold text-lg mb-2">04</div>
                            <h3 class="font-bold text-foreground mb-2">Go-Live Readiness</h3>
                            <p class="text-muted-foreground text-sm">End-to-end test until stable + handover pack. You're operational with full documentation.</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Operational Delivery Commitment Section -->
            <section class="section-padding bg-background">
                <div class="max-w-4xl mx-auto px-6">
                    <div class="bg-card rounded-xl border border-border p-8 md:p-12 text-center">
                        <div class="w-16 h-16 rounded-xl bg-primary flex items-center justify-center mb-6 mx-auto">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-shield w-8 h-8 text-primary-foreground"><path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"></path></svg>
                        </div>
                        <h2 class="text-3xl md:text-4xl font-bold text-foreground mb-4">Operational Delivery Commitment</h2>
                        <p class="text-muted-foreground text-lg mb-8">Within 40 business days of payment, for the agreed rollout scope:</p>
                        <div class="grid sm:grid-cols-2 gap-4 text-left max-w-2xl mx-auto mb-8">
                            <div class="flex items-start gap-3 bg-accent rounded-lg p-4">
                                <span class="text-primary">✓</span>
                                <span class="text-foreground text-sm">100% contact-attempt coverage across the approved debtor list</span>
                            </div>
                            <div class="flex items-start gap-3 bg-accent rounded-lg p-4">
                                <span class="text-primary">✓</span>
                                <span class="text-foreground text-sm">Auditable evidence logs for attempts, timestamps, and outcomes</span>
                            </div>
                            <div class="flex items-start gap-3 bg-accent rounded-lg p-4">
                                <span class="text-primary">✓</span>
                                <span class="text-foreground text-sm">30 days of remediation for delivery gaps</span>
                            </div>
                            <div class="flex items-start gap-3 bg-accent rounded-lg p-4">
                                <span class="text-primary">✓</span>
                                <span class="text-foreground text-sm">Implementation fee reimbursement if standards remain unmet</span>
                            </div>
                        </div>
                        <button class="inline-flex items-center justify-center gap-2 bg-primary text-primary-foreground hover:bg-primary/90 font-semibold px-10 py-4 rounded-lg text-base transition-all duration-300 shadow-lg">See If It Fits</button>
                    </div>
                </div>
            </section>

          
        </main>
        """,
        "css": """
        .min-h-screen { min-height: 100vh; }
        .bg-background { background-color: #ffffff; }
        .text-foreground { color: #000000; }
        .overflow-x-hidden { overflow-x: hidden; }
        .relative { position: relative; }
        .overflow-hidden { overflow: hidden; }
        .flex { display: flex; }
        .items-center { align-items: center; }
        .justify-between { justify-content: space-between; }
        .px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
        .py-5 { padding-top: 1.25rem; padding-bottom: 1.25rem; }
        .max-w-7xl { max-width: 80rem; }
        .mx-auto { margin-left: auto; margin-right: auto; }
        .gap-3 { gap: 0.75rem; }
        .h-9 { height: 2.25rem; }
        .font-bold { font-weight: 700; }
        .text-lg { font-size: 1.125rem; line-height: 1.75rem; }
        .tracking-tight { letter-spacing: -0.025em; }
        .hidden { display: none; }
        .md\\:inline-flex { display: inline-flex; }
        .text-muted-foreground { color: #6b7280; }
        .hover\\:text-foreground:hover { color: #000000; }
        .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
        .bg-primary { background-color: #2563eb; }
        .text-primary-foreground { color: #ffffff; }
        .hover\\:bg-primary\\/90:hover { background-color: rgba(37, 99, 235, 0.9); }
        .px-5 { padding-left: 1.25rem; padding-right: 1.25rem; }
        .py-2\\.5 { padding-top: 0.625rem; padding-bottom: 0.625rem; }
        .text-base { font-size: 1rem; line-height: 1.5rem; }
        .ml-1\\.5 { margin-left: 0.375rem; }
        .text-center { text-align: center; }
        .pt-8 { padding-top: 2rem; }
        .pb-6 { padding-bottom: 1.5rem; }
        .md\\:pt-12 { padding-top: 3rem; }
        .md\\:pb-8 { padding-bottom: 2rem; }
        .max-w-4xl { max-width: 56rem; }
        .inline-flex { display: inline-flex; }
        .bg-accent { background-color: #f3f4f6; }
        .text-accent-foreground { color: #111827; }
        .rounded-full { border-radius: 9999px; }
        .mb-8 { margin-bottom: 2rem; }
        .w-2 { width: 0.5rem; }
        .h-2 { height: 0.5rem; }
        .rounded-full { border-radius: 9999px; }
        .bg-primary { background-color: #2563eb; }
        .text-4xl { font-size: 2.25rem; line-height: 2.5rem; }
        .md\\:text-5xl { font-size: 3rem; line-height: 1; }
        .lg\\:text-6xl { font-size: 3.75rem; line-height: 1; }
        .leading-\\[1\\.1\\] { line-height: 1.1; }
        .tracking-tight { letter-spacing: -0.025em; }
        .text-primary { color: #2563eb; }
        .text-lg { font-size: 1.125rem; line-height: 1.75rem; }
        .md\\:text-xl { font-size: 1.25rem; line-height: 1.75rem; }
        .max-w-2xl { max-width: 42rem; }
        .mb-10 { margin-bottom: 2.5rem; }
        .leading-relaxed { line-height: 1.625; }
        .flex-col { flex-direction: column; }
        .sm\\:flex-row { flex-direction: row; }
        .justify-center { justify-content: center; }
        .gap-4 { gap: 1rem; }
        .mb-6 { margin-bottom: 1.5rem; }
        .px-8 { padding-left: 2rem; padding-right: 2rem; }
        .py-6 { padding-top: 1.5rem; padding-bottom: 1.5rem; }
        .font-semibold { font-weight: 600; }
        .shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
        .shadow-primary\\/20 { box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.2), 0 4px 6px -2px rgba(37, 99, 235, 0.1); }
        .border { border-width: 1px; }
        .bg-transparent { background-color: transparent; }
        .hover\\:border-primary\\/50:hover { border-color: rgba(37, 99, 235, 0.5); }
        .border-border { border-color: #e5e7eb; }
        .hover\\:bg-secondary:hover { background-color: #f9fafb; }
        .py-6 { padding-top: 1.5rem; padding-bottom: 1.5rem; }
        .text-sm { font-size: 0.875rem; line-height: 1.25rem; }
        .font-medium { font-weight: 500; }
        .tracking-wide { letter-spacing: 0.05em; }
        .uppercase { text-transform: uppercase; }
        .mb-6 { margin-bottom: 1.5rem; }
        .flex-wrap { flex-wrap: wrap; }
        .gap-x-10 { column-gap: 2.5rem; }
        .gap-y-4 { row-gap: 1rem; }
        .px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
        .text-muted-foreground\\/60 { color: rgba(107, 114, 128, 0.6); }
        .font-bold { font-weight: 700; }
        .tracking-widest { letter-spacing: 0.1em; }
        .bg-secondary\\/50 { background-color: rgba(243, 244, 246, 0.5); }
        .max-w-6xl { max-width: 72rem; }
        .grid { display: grid; }
        .md\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .lg\\:grid-cols-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
        .gap-6 { gap: 1.5rem; }
        .rounded-xl { border-radius: 0.75rem; }
        .border { border-width: 1px; }
        .transition-all { transition-property: all; transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1); transition-duration: 150ms; }
        .hover\\:border-primary\\/30:hover { border-color: rgba(37, 99, 235, 0.3); }
        .hover\\:shadow-md:hover { box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); }
        .w-11 { width: 2.75rem; }
        .h-11 { height: 2.75rem; }
        .mb-5 { margin-bottom: 1.25rem; }
        .bg-accent { background-color: #f3f4f6; }
        .text-primary { color: #2563eb; }
        .w-5 { width: 1.25rem; }
        .h-5 { height: 1.25rem; }
        .shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
        .grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .md\\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
        .lg\\:grid-cols-6 { grid-template-columns: repeat(6, minmax(0, 1fr)); }
        .gap-4 { gap: 1rem; }
        .text-2xl { font-size: 1.5rem; line-height: 2rem; }
        .md\\:text-3xl { font-size: 1.875rem; line-height: 2.25rem; }
        .text-xs { font-size: 0.75rem; line-height: 1rem; }
        .space-y-12 { --tw-space-y-reverse: 0; margin-top: calc(3rem * calc(1 - var(--tw-space-y-reverse))); margin-bottom: calc(3rem * var(--tw-space-y-reverse)); }
        .aspect-video { aspect-ratio: 16 / 9; }
        .overflow-hidden { overflow: hidden; }
        .border-border { border-color: #e5e7eb; }
        .shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05); }
        .shadow-2xl { box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
        .shadow-primary\\/10 { box-shadow: 0 25px 50px -12px rgba(37, 99, 235, 0.1); }
        .bg-background { background-color: #ffffff; }
        .flex-1 { flex: 1 1 0%; }
        .justify-center { justify-content: center; }
        .gap-2 { gap: 0.5rem; }
        .px-4 { padding-left: 1rem; padding-right: 1rem; }
        .py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
        .bg-accent { background-color: #f3f4f6; }
        .border-b { border-bottom-width: 1px; }
        .rounded-md { border-radius: 0.375rem; }
        .px-4 { padding-left: 1rem; padding-right: 1rem; }
        .py-1 { padding-top: 0.25rem; padding-bottom: 0.25rem; }
        .text-xs { font-size: 0.75rem; line-height: 1rem; }
        .font-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
        .sm\\:grid-cols-2 { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        .lg\\:grid-cols-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
        .gap-5 { gap: 1.25rem; }
        .py-12 { padding-top: 3rem; padding-bottom: 3rem; }
        .w-16 { width: 4rem; }
        .h-16 { height: 4rem; }
        .rounded-xl { border-radius: 0.75rem; }
        .bg-primary { background-color: #2563eb; }
        .items-center { align-items: center; }
        .justify-center { justify-content: center; }
        .mb-6 { margin-bottom: 1.5rem; }
        .mx-auto { margin-left: auto; margin-right: auto; }
        .w-8 { width: 2rem; }
        .h-8 { height: 2rem; }
        .py-12 { padding-top: 3rem; padding-bottom: 3rem; }
        .border-t { border-top-width: 1px; }
        .py-8 { padding-top: 2rem; padding-bottom: 2rem; }
        .pt-8 { padding-top: 2rem; }
        .border-t { border-top-width: 1px; }
        .text-center { text-align: center; }
        """
    }
    
    try:
        # Update the existing page or create a new one with all sections
        page, created = Page.objects.update_or_create(
            slug='demo',
            defaults={
                'title': 'Demo Page',
                'status': 'published',
                'blocks_json': complete_content
            }
        )
        print("✓ Demo page updated successfully with all sections!")
        print(f"Page URL: /demo/")
        print("Sections added:")
        print("1. One Platform for Compliant AI Collections")
        print("2. Real Results From a Live Portfolio")
        print("3. Hear From a Law Bureau Running Live Collections")
        print("4. Transform Your Debt Collection With Our Compliant AI Solution")
        print("5. How It Works")
        print("6. Operational Delivery Commitment")
        print("7. Footer")
        return True
    except Exception as e:
        print(f"✗ Error updating demo page: {e}")
        return False


if __name__ == "__main__":
    print("Demo Page Update Script")
    print("=" * 50)
    
    success = update_demo_page_with_sections()
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 DEMO PAGE UPDATED WITH ALL SECTIONS!")
        print("=" * 50)
        print("\n📋 Sections Added:")
        print("1. ✅ One Platform for Compliant AI Collections")
        print("2. ✅ Real Results From a Live Portfolio")
        print("3. ✅ Hear From a Law Bureau Running Live Collections")
        print("4. ✅ Transform Your Debt Collection With Our Compliant AI Solution")
        print("5. ✅ How It Works")
        print("6. ✅ Operational Delivery Commitment")
        print("7. ✅ Footer")
        print("\n🚀 Next steps:")
        print("1. Visit: http://localhost:8000/demo/ to see the updated page")
        print("2. Or use the admin panel to further customize with GrapesJS editor")
    else:
        print("\n❌ Failed to update demo page. Please check the implementation.")
        sys.exit(1)