from markers.models import Marker
from .classification_model import CountCars
from markers.models import Marker
import cv2
from urllib.request import urlopen
import numpy as np

countCars = CountCars()

def getCarsFromImage():
    allMarkers = Marker.objects.all()

    for marker in allMarkers:
        #print("CAM: " + str(marker.camera) + " NOME: " + str(marker.name))

        try:
            req = urlopen("http://transito.gtrans.com.br/cttupe/index.php/portal/getImg/" + marker.camera)
            arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
            im = cv2.imdecode(arr, -1)
        
            marker.parkspace = countCars.count(im)
            #marker.save()
        except:
            marker.parkspace = 0

        marker.save()

    

def updateMarkers():
    print("[START] map updater")
    getCarsFromImage()
    print("[STOP] map updater")