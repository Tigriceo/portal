from django.contrib.gis.geoip2 import GeoIP2


# Геолокация - определение города по ip
# TODO: раскомментировать строки 14,15,16,17 при выкладывании на сервер
def location_geoip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip)
    # g = GeoIP2()
    # location = g.city(ip)
    # location_city = location["city"]
    # return location_city
