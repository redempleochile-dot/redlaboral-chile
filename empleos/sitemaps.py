from django.contrib.sitemaps import Sitemap
from .models import OfertaLaboral

class OfertaSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8

    def items(self):
        return OfertaLaboral.objects.filter(publicada=True).order_by('-fecha_publicacion')

    def lastmod(self, obj):
        return obj.fecha_publicacion