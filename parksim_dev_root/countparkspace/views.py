from django.shortcuts import render
from markers.models import Marker
from django.contrib.gis.geos import GEOSGeometry
from .form import InputForm
from .service.classification_model import CountCars
import pandas as pd
import json
from django.http import HttpResponse
import ast

import cv2
from urllib.request import urlopen
import numpy as np


countCars = CountCars()

def countParkSpaceView(request):
    if request.method == 'POST':
        form = InputForm(request.POST, request.FILES)
    
        name = form.data['name']
        #location = ast.literal_eval(form.data['location'])
        #print("\n\n\n\n\n\nSRID: ", GEOSGeometry(json.dumps(location)), "\n\n\n\n\n")
        lat = form.data['lat']
        lon = form.data['lon']
        
        parkspace = countCars.count(img = request.FILES['parkspace'])
        
        # Avenida Caxanga: -34.934157 -8.043131
        print("\n\nName: " + str(name) + "\nLocation: " + lat + " _ " + lon + "\n", GEOSGeometry('POINT(%s %s)' % (lon, lat), srid=4326),"\n\nParkSpace VAGAS: " + str(parkspace))
    
        Marker.objects.create(name=name, location=GEOSGeometry('POINT(%s %s)' % (lon, lat), srid=4326), parkspace=parkspace)

        form = InputForm()
        context = {
            'form': form,
        }
        return render(request, 'countparkspace/countparkspace.html', context)
        
    else:
        # I used that to get the cameras of cttu recife
        '''        
        df = pd.read_csv('countparkspace/cameras_coordenadas.txt', delimiter = ";")
        
        for i in range(0,len(df)):
            name = df['nome'][i]
            lat = df['lat'][i]
            lon = df['lon'][i]
            camera = df['ip'][i]
            parkspace = 10

            Marker.objects.create(name=name, location=GEOSGeometry('POINT(%s %s)' % (lon, lat), srid=4326), camera=camera, parkspace=parkspace)

            print("\n\nName: " + str(name) + "\nLocation: " + str(lat) + " _ " + str(lon) + "\n", GEOSGeometry('POINT(%s %s)' % (lon, lat), srid=4326),"\n\nParkSpace VAGAS: " + str(parkspace))

        #Marker.objects.all().delete()
        #print(df.dtypes)
        return HttpResponse("<p>Name: " + str(name) + " Location: " + str(lat) + "</p>")
        '''
        
        allMarkers = Marker.objects.all()
        print("\n\nINICIANDO CAPTURA DE IMAGENS...\n\n")

        for marker in allMarkers:
            print("CAM: " + str(marker.camera) + " NOME: " + str(marker.name))

            try:
                req = urlopen("http://transito.gtrans.com.br/cttupe/index.php/portal/getImg/" + marker.camera)
                arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
                im = cv2.imdecode(arr, -1)
            
                marker.parkspace = countCars.count(im)
                #marker.save()
            except:
                marker.parkspace = 0

            marker.save()

        print("\n\nFINALIZANDO CAPTURA DE IMAGENS...\n\n")

        form = InputForm()
        context = {
            'form': form,
        }
        #assert False
        return render(request, 'countparkspace/countparkspace.html', context)
