from django.contrib.sites.shortcuts import get_current_site

from config import settings


def site_data_from_request(request) -> dict:
    """
    Получение данных о сайте из request и добавление их в словарь для
    последуюзего переиспользования.
    """
    context = {}
    site = get_current_site(request)
    domain = getattr(settings, "DOMAIN", "") or site.domain
    protocol = "https" if request.is_secure() else "http"
    site_name = getattr(settings, "SITE_NAME", "") or site.name
    context.update(
        {
            "domain": domain,
            "protocol": protocol,
            "site_name": site_name,
        }
    )
    return context
