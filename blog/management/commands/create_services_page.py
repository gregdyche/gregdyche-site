from django.core.management.base import BaseCommand
from blog.models import Page, PageCategory

class Command(BaseCommand):
    help = 'Create a professional services page for consulting offerings'

    def handle(self, *args, **options):
        # Create or get services page
        services_page, created = Page.objects.get_or_create(
            slug='services',
            defaults={
                'title': 'Services & Consulting',
                'content': self.get_services_content(),
                'is_published': True,
                'show_in_toc': True,
                'toc_order': 1,
                'meta_description': 'Professional consulting services in technology, education, and life management from Greg Dyche.',
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created services page (ID: {services_page.id})')
            )
        else:
            # Update content
            services_page.content = self.get_services_content()
            services_page.save()
            self.stdout.write(
                self.style.SUCCESS('✓ Updated services page content')
            )
        
        self.stdout.write(f'Services page URL: /blog/page/{services_page.slug}/')

    def get_services_content(self):
        """Professional services page content"""
        return '''
<div class="services-hero">
    <h1 style="font-size: 3rem; font-weight: 800; color: var(--text-primary); margin-bottom: 1.5rem; text-align: center;">
        Services & Consulting
    </h1>
    <p style="font-size: 1.25rem; color: var(--text-secondary); text-align: center; max-width: 700px; margin: 0 auto 3rem;">
        Transform your technology, education, and life management challenges into opportunities for growth
    </p>
</div>

<!-- Core Services -->
<section style="margin-bottom: 4rem;">
    <h2 style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 2rem; text-align: center;">
        Core Services
    </h2>
    
    <div class="grid grid-cols-1 md:grid-cols-3" style="gap: 2rem;">
        <!-- Technology Consulting -->
        <div class="card" style="padding: 2rem;">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">💻</div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: var(--tech-accent); margin-bottom: 1rem;">
                    Technology Consulting
                </h3>
            </div>
            <ul style="list-style: none; padding: 0; margin-bottom: 2rem;">
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--tech-accent);">✓</span>
                    Python development & automation
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--tech-accent);">✓</span>
                    Django web application development
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--tech-accent);">✓</span>
                    AI/ML integration & workflows
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--tech-accent);">✓</span>
                    Development workflow optimization
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--tech-accent);">✓</span>
                    Technical architecture reviews
                </li>
            </ul>
            <p style="font-weight: 600; color: var(--tech-accent); text-align: center;">
                Starting at $150/hour
            </p>
        </div>

        <!-- Educational Consulting -->
        <div class="card" style="padding: 2rem;">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎓</div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: var(--life-accent); margin-bottom: 1rem;">
                    Educational Consulting
                </h3>
            </div>
            <ul style="list-style: none; padding: 0; margin-bottom: 2rem;">
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--life-accent);">✓</span>
                    Curriculum development & design
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--life-accent);">✓</span>
                    Educational technology integration
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--life-accent);">✓</span>
                    Learning management system setup
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--life-accent);">✓</span>
                    Faculty development & training
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--life-accent);">✓</span>
                    Assessment strategy design
                </li>
            </ul>
            <p style="font-weight: 600; color: var(--life-accent); text-align: center;">
                Starting at $125/hour
            </p>
        </div>

        <!-- Life Management Coaching -->
        <div class="card" style="padding: 2rem;">
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🎯</div>
                <h3 style="font-size: 1.5rem; font-weight: 600; color: var(--spirit-accent); margin-bottom: 1rem;">
                    Life Management Coaching
                </h3>
            </div>
            <ul style="list-style: none; padding: 0; margin-bottom: 2rem;">
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Productivity system design
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Personal workflow optimization
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Goal setting & achievement strategies
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Digital minimalism & focus
                </li>
                <li style="margin-bottom: 0.75rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Intentional living practices
                </li>
            </ul>
            <p style="font-weight: 600; color: var(--spirit-accent); text-align: center;">
                Starting at $100/hour
            </p>
        </div>
    </div>
</section>

<!-- Virtual Sessions -->
<section style="margin-bottom: 4rem; background: rgba(255, 255, 255, 0.1); padding: 3rem 2rem; border-radius: 12px;">
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 1rem;">
            Virtual Coaching Sessions
        </h2>
        <p style="font-size: 1.2rem; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">
            One-on-one virtual sessions designed to help you break through challenges and optimize your approach
        </p>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-2" style="gap: 2rem; max-width: 800px; margin: 0 auto;">
        <div class="card" style="padding: 2rem; text-align: center;">
            <h3 style="font-size: 1.5rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1rem;">
                Strategy Session
            </h3>
            <p style="font-size: 3rem; font-weight: 700; color: var(--spirit-accent); margin-bottom: 1rem;">
                $150
            </p>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                90-minute deep-dive session to tackle your biggest challenge and create an actionable plan
            </p>
            <ul style="list-style: none; padding: 0; text-align: left;">
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Problem analysis & goal clarification
                </li>
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Custom strategy development
                </li>
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Implementation roadmap
                </li>
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Follow-up resource recommendations
                </li>
            </ul>
        </div>
        
        <div class="card" style="padding: 2rem; text-align: center;">
            <h3 style="font-size: 1.5rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1rem;">
                Quick Consultation
            </h3>
            <p style="font-size: 3rem; font-weight: 700; color: var(--spirit-accent); margin-bottom: 1rem;">
                $75
            </p>
            <p style="color: var(--text-secondary); margin-bottom: 1.5rem;">
                45-minute focused session for specific questions or quick problem-solving
            </p>
            <ul style="list-style: none; padding: 0; text-align: left;">
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Rapid problem assessment
                </li>
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Expert guidance & recommendations
                </li>
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Next steps clarification
                </li>
                <li style="margin-bottom: 0.5rem; padding-left: 1.5rem; position: relative;">
                    <span style="position: absolute; left: 0; color: var(--spirit-accent);">✓</span>
                    Resource sharing
                </li>
            </ul>
        </div>
    </div>
</section>

<!-- Process -->
<section style="margin-bottom: 4rem;">
    <h2 style="font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 2rem; text-align: center;">
        How It Works
    </h2>
    
    <div class="grid grid-cols-1 md:grid-cols-3" style="gap: 2rem;">
        <div style="text-align: center;">
            <div style="width: 60px; height: 60px; background: var(--spirit-accent); color: var(--creighton-navy); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; margin: 0 auto 1rem;">1</div>
            <h3 style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1rem;">Initial Contact</h3>
            <p style="color: var(--text-secondary);">Reach out via email or contact form to discuss your needs and goals</p>
        </div>
        
        <div style="text-align: center;">
            <div style="width: 60px; height: 60px; background: var(--spirit-accent); color: var(--creighton-navy); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; margin: 0 auto 1rem;">2</div>
            <h3 style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1rem;">Scope & Schedule</h3>
            <p style="color: var(--text-secondary);">We'll define the project scope, timeline, and schedule your sessions</p>
        </div>
        
        <div style="text-align: center;">
            <div style="width: 60px; height: 60px; background: var(--spirit-accent); color: var(--creighton-navy); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.5rem; font-weight: 700; margin: 0 auto 1rem;">3</div>
            <h3 style="font-size: 1.25rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1rem;">Execute & Deliver</h3>
            <p style="color: var(--text-secondary);">Get results through focused collaboration and actionable solutions</p>
        </div>
    </div>
</section>

<!-- CTA -->
<section style="background: linear-gradient(135deg, var(--spirit-accent), #e6b025); padding: 3rem 2rem; border-radius: 12px; text-align: center;">
    <h2 style="font-size: 2.5rem; font-weight: 700; color: var(--creighton-navy); margin-bottom: 1rem;">
        Ready to Get Started?
    </h2>
    <p style="font-size: 1.2rem; color: var(--creighton-navy); margin-bottom: 2rem; opacity: 0.9;">
        Let's discuss how I can help you achieve your technology, education, or life management goals
    </p>
    <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap;">
        <a href="/blog/page/contact/" style="background: var(--creighton-navy); color: white; padding: 1rem 2rem; border-radius: 8px; text-decoration: none; font-weight: 600; transition: all 0.2s ease; display: inline-block;">
            Start a Conversation
        </a>
        <a href="mailto:gregdyche@gmail.com?subject=Consulting Inquiry" style="background: transparent; color: var(--creighton-navy); padding: 1rem 2rem; border: 2px solid var(--creighton-navy); border-radius: 8px; text-decoration: none; font-weight: 600; transition: all 0.2s ease; display: inline-block;">
            Email Directly
        </a>
    </div>
    <p style="font-size: 0.9rem; color: var(--creighton-navy); margin-top: 1.5rem; opacity: 0.8;">
        Invoicing handled separately • Virtual sessions via Zoom • Flexible scheduling
    </p>
</section>
        '''.strip()