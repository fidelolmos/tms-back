from django.db import models
from django.conf import settings
from geopy.geocoders import Nominatim
import requests
from django.contrib.auth import get_user_model


User = get_user_model()

# Modelo de Direcciones
class Direction(models.Model):
    name = models.CharField(max_length=255, blank=True)
    street = models.CharField(max_length=255, blank=True)
    interior = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, blank=True)
    lat = models.FloatField(blank=True, null=True)
    lon = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.lat or not self.lon:
            self.obtain_geolocation()
        super().save(*args, **kwargs)
    
    def obtain_geolocation(self):
        geolocator = Nominatim(user_agent="django_geocoder")
        address_query = ", ".join(filter(None, [self.street, self.city, self.state, self.zip_code, self.country]))
        if address_query:
            location = geolocator.geocode(address_query)
            if location:
                self.lat = location.latitude
                self.lon = location.longitude

    def __str__(self):
        return self.name or self.street

# Modelo de Orden de Transporte
class Order(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=True)
    date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    origin = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='orders_origin')
    destination = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='orders_destination')
    delivery_address = models.ForeignKey(Direction, on_delete=models.SET_NULL, related_name='orders_delivery', null=True, blank=True)
    description = models.TextField(blank=True)
    delivery_contact = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = f"ORD-{self.pk}"  # Generación de código de orden
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

# Modelo de Rutas de viaje
class Route(models.Model):
    name = models.CharField(max_length=255)
    origin = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='routes_origin')
    destination = models.ForeignKey(Direction, on_delete=models.CASCADE, related_name='routes_destination')
    distance = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.distance:
            self.calculate_distance()
        super().save(*args, **kwargs)
    
    def calculate_distance(self):
        if self.origin and self.destination and self.origin.lat and self.origin.lon and self.destination.lat and self.destination.lon:
            try:
                url = (
                    f"http://router.project-osrm.org/route/v1/driving/"
                    f"{self.origin.lon},{self.origin.lat};"
                    f"{self.destination.lon},{self.destination.lat}?overview=false"
                )
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    data = response.json()
                    if 'routes' in data and data['routes']:
                        self.distance = data['routes'][0]['distance'] / 1000.0  # Convertir a km
                    else:
                        self.distance = 0.0
            except:
                self.distance = 0.0
    
    def __str__(self):
        return self.name

# Modelo de Transporte
class TMS(models.Model):
    name = models.CharField(max_length=100, unique=True)
    vehicle = models.CharField(max_length=100)
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tms_driver')
    single_route = models.BooleanField(default=False)
    planned_routes = models.ManyToManyField(Route, related_name='tms_routes', blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    bill_of_lading = models.FileField(upload_to='bills/', null=True, blank=True)
    total_distance = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.calculate_total_distance()
        super().save(*args, **kwargs)
    
    def calculate_total_distance(self):
        self.total_distance = sum(route.distance for route in self.planned_routes.all() if route.distance)
    
    def __str__(self):
        return self.name
