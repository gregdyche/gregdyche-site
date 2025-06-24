from django.core.management.base import BaseCommand
from blog.models import Page, PageCategory

class Command(BaseCommand):
    help = 'Create a homepage Page object from the current homepage template'

    def handle(self, *args, **options):
        # Check if homepage already exists
        homepage, created = Page.objects.get_or_create(
            slug='homepage',
            defaults={
                'title': 'Well Scripted Life',
                'content': self.get_homepage_content(),
                'is_published': True,
                'show_in_toc': False,  # Don't show in TOC
                'toc_order': 0,
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created homepage Page object (ID: {homepage.id})')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'! Homepage Page already exists (ID: {homepage.id})')
            )
            # Update content if needed
            homepage.content = self.get_homepage_content()
            homepage.save()
            self.stdout.write(
                self.style.SUCCESS('✓ Updated homepage content')
            )
        
        self.stdout.write(f'Homepage slug: {homepage.slug}')
        self.stdout.write(f'Homepage URL: /blog/page/{homepage.slug}/')

    def get_homepage_content(self):
        """Extract the main content from the homepage template"""
        return '''
<div class="container mt-8">
    <!-- Personal Hero Section -->
    <section class="hero">
        <div style="text-align: center; margin-bottom: 3rem;">
            <h1 style="font-size: 3.5rem; font-weight: 800; color: var(--text-primary); margin-bottom: 1rem; line-height: 1.2;">
                Well Scripted Life
            </h1>
            <p style="font-size: 1.5rem; color: var(--text-muted); margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">
                Modern insights on technology, education, and intentional living
            </p>
            <p style="font-size: 1.2rem; color: var(--text-secondary); font-weight: 500;">
                by Greg Dyche
            </p>
        </div>
    </section>
    
    <!-- Personal Introduction -->
    <section style="margin-bottom: 4rem;">
        <div class="card" style="max-width: 800px; margin: 0 auto;">
            <div class="card-content" style="font-size: 1.1rem; line-height: 1.7;">
                <p style="font-size: 1.3rem; font-weight: 600; color: var(--text-primary); margin-bottom: 1.5rem;">
                    Hi, I'm Greg Dyche — educator, developer, and lifelong learner.
                </p>
                
                <p style="margin-bottom: 1.5rem;">
                    This is where I share insights on the intersection of technology, education, and intentional living. 
                    I bring together experience from education and technology, having worked as both an educator and developer.
                </p>
                
                <p style="margin-bottom: 1.5rem;">
                    I'm passionate about creating efficient, elegant solutions to complex problems, helping others learn and grow in their technical skills, building systems that support human flourishing, and living with intention and purpose.
                </p>
                
                <p style="margin-bottom: 0;">
                    Whether you're here for the code, the productivity tips, or the deeper reflections on life, I'm glad you're here. 
                    Welcome to the journey.
                </p>
            </div>
        </div>
    </section>

    <!-- What You'll Find Here -->
    <section style="margin-bottom: 4rem;">
        <h2 style="text-center; font-size: 2.5rem; font-weight: 700; color: var(--text-primary); margin-bottom: 2rem;">
            What You'll Find Here
        </h2>
        <div class="grid grid-cols-3">
            <a href="/blog/tech/" class="card card-clickable">
                <div class="card-header">
                    <h3 class="card-title">Technology</h3>
                    <p class="card-subtitle">Code, Tools & Innovation</p>
                </div>
                <p class="card-content">Python development, AI/ML insights, development workflows, and emerging technologies that are shaping our world.</p>
            </a>
            
            <a href="/blog/life/" class="card card-clickable">
                <div class="card-header">
                    <h3 class="card-title">Life Management</h3>
                    <p class="card-subtitle">Systems & Productivity</p>
                </div>
                <p class="card-content">Personal productivity systems, educational strategies, and practical workflows for getting things done.</p>
            </a>
            
            <a href="/blog/spirit/" class="card card-clickable">
                <div class="card-header">
                    <h3 class="card-title">Spiritual Growth</h3>
                    <p class="card-subtitle">Faith & Reflection</p>
                </div>
                <p class="card-content">Reflections on faith, intentional living, and finding meaning in our daily work and relationships.</p>
            </a>
        </div>
    </section>
    
    <!-- Newsletter Subscription -->
    <section style="margin-bottom: 4rem;">
        <div class="card" style="max-width: 700px; margin: 0 auto; background: linear-gradient(135deg, var(--accent-color), var(--accent-hover)); color: white;">
            <div class="card-content" style="text-align: center; padding: 3rem 2rem;">
                <h2 style="font-size: 2.2rem; font-weight: 700; margin-bottom: 1rem; color: white;">
                    Stay Updated
                </h2>
                <p style="font-size: 1.2rem; margin-bottom: 2rem; opacity: 0.9;">
                    Get notified when I publish new insights on technology, life management, and spiritual growth.
                </p>
                
                <div style="display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-bottom: 1.5rem;">
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                        📚 Tech Insights
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                        🎯 Life Systems
                    </span>
                    <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.9rem;">
                        🌱 Spiritual Growth
                    </span>
                </div>
                
                <a href="/blog/subscribe/" class="btn" style="background: white; color: var(--accent-color); padding: 1rem 2rem; font-weight: 700; border-radius: 8px; text-decoration: none; display: inline-block; transition: all 0.2s;">
                    Subscribe to Updates
                </a>
                
                <p style="font-size: 0.85rem; margin-top: 1rem; opacity: 0.8;">
                    No spam, unsubscribe anytime. Choose only the topics you're interested in.
                </p>
            </div>
        </div>
    </section>

    <!-- Quick Access -->
    <section style="margin-bottom: 4rem;">
        <h2 style="text-center; font-size: 2rem; font-weight: 700; color: var(--text-primary); margin-bottom: 2rem;">
            Quick Access
        </h2>
        <div class="grid grid-cols-3">
            <a href="/blog/page/about/" class="card card-clickable">
                <div class="card-header">
                    <h3 class="card-title">About Greg</h3>
                    <p class="card-subtitle">Background & Philosophy</p>
                </div>
                <p class="card-content">Learn about my background in education, technology, and life philosophy.</p>
            </a>
            
            <a href="/blog/page/tech-stack/" class="card card-clickable">
                <div class="card-header">
                    <h3 class="card-title">Tech Stack</h3>
                    <p class="card-subtitle">Tools & Setup</p>
                </div>
                <p class="card-content">My development environment, favorite tools, and technical workflows.</p>
            </a>
            
            <a href="/blog/page/contact/" class="card card-clickable">
                <div class="card-header">
                    <h3 class="card-title">Let's Connect</h3>
                    <p class="card-subtitle">Get in Touch</p>
                </div>
                <p class="card-content">Questions, collaborations, or just want to say hello? Don't hesitate to reach out.</p>
            </a>
        </div>
    </section>
</div>
        '''.strip()