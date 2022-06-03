from django.contrib.gis import forms
from django.conf import settings

# creating a form
class InputForm(forms.Form):
    name = forms.CharField(max_length=255)
    # location = forms.PointField(widget=forms.OSMWidget(attrs={'map_width': 800,
    # 'map_height': 500,
    # 'default_lat': -8.038198,
    # 'default_lon':-34.947881,
    # 'default_zoom': 15,}))
    lat = forms.CharField(max_length=255)
    lon = forms.CharField(max_length=255)
    parkspace = forms.ImageField()
