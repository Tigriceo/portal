from django import template
import geoip2.database
from geoip2.errors import AddressNotFoundError

register = template.Library()


@register.simple_tag(takes_context=True)
def location_geoip(context):
    """Геолокация - определение города по ip"""
    x_forwarded_for = context['request'].META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = context['request'].META.get('REMOTE_ADDR')
    print(ip)
    # g = GeoIP2()
    # location = g.city(ip)
    # location_city = location["city"]
    reader = geoip2.database.Reader('service/geoip/GeoLite2-City.mmdb')
    try:
        response = reader.city(ip)
        location_city = response.city.names['ru']
        print(location_city)
        reader.close()
        return location_city
    except AddressNotFoundError:
        return "не определен"
