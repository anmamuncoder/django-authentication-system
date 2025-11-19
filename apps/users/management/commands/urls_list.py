from django.core.management.base import BaseCommand
from django.urls import URLPattern, URLResolver, get_resolver

class Command(BaseCommand):
    help = "List all URL patterns"

    def handle(self, *args, **options):
        resolver = get_resolver().url_patterns
        self.print_urls(resolver)

    def print_urls(self, patterns, prefix=""):
        for p in patterns:
            if isinstance(p, URLPattern):   # normal endpoint
                print(prefix + str(p.pattern))
            elif isinstance(p, URLResolver):  # included urls
                self.print_urls(p.url_patterns, prefix + str(p.pattern))
 