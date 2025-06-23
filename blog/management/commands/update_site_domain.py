from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

class Command(BaseCommand):
    help = 'Update the Django site domain to fix "View on site" links'

    def add_arguments(self, parser):
        parser.add_argument(
            '--domain',
            type=str,
            default='site-setup-production.up.railway.app',
            help='Domain to set for the site'
        )

    def handle(self, *args, **options):
        domain = options['domain']
        
        try:
            site = Site.objects.get(id=1)
            old_domain = site.domain
            site.domain = domain
            site.name = 'Greg Dyche - Well Scripted Life'
            site.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated site domain from "{old_domain}" to "{domain}"'
                )
            )
        except Site.DoesNotExist:
            self.stdout.write(
                self.style.ERROR('Site with ID 1 does not exist')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error updating site: {e}')
            )