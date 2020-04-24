from django.contrib.gis.geoip2 import GeoIP2
import geoip2.database


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

    # reader = geoip2.database.Reader('service/geoip/GeoLite2-City.mmdb')
    # response = reader.city(ip)
    # location_city = response.city.names['ru']
    # print(location_city)
    # reader.close()
    # return location_city
