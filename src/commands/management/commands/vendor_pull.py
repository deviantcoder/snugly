from utils.downloader import download_vendor_static

from django.core.management.base import BaseCommand
from django.conf import settings


STATICFILES_VENDOR_DIR = getattr(settings, 'STATICFILES_VENDOR_DIR')
VENDOR_FILES = {
    'bootstrap.min.css': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'comfortaa.css': 'https://fonts.googleapis.com/css2?family=Comfortaa:wght@300;400;700&display=swap',
    'bootstrap.bundle.min.js': 'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
}


class Command(BaseCommand):
    """
    Management command to download CDN vendor static files.
    """

    def handle(self, *args, **kwargs):
        self.stdout.write('Downloading CDN vendor static files...')

        completed_urls = []

        for filename, url in VENDOR_FILES.items():
            out_path = STATICFILES_VENDOR_DIR / filename

            download_status = download_vendor_static(url, out_path, parent_mkdir=True)

            if download_status:
                completed_urls.append(url)
            else:
                self.stdout.write(self.style.ERROR(f'Failed to download {url}'))

        if set(completed_urls) == set(VENDOR_FILES.values()):
            self.stdout.write(self.style.SUCCESS('All vendor static files were downloaded successfully'))
        else:
            self.stderr.write(self.style.ERROR('Some vendor static files failed to download'))
