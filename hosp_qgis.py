import qgis
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
from qgis.core import *
from qgis.gui import *
from qgis.utils import *
import sys
import os
from qgis.analysis import QgsNativeAlgorithms

#   Instantiate the QGIS Application
GUIEnabled = False
app = QgsApplication([], GUIEnabled)
#   Update prefix path
app.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
app.initQgis()

uri = "C:/ODK Briefcase/Exports/Hospital_final.csv"
vlayer = QgsVectorLayer("C:/ODK Briefcase/Exports/Hospital_final.csv", "Hosp_final", "ogr")
path = "http://server.arcgisonline.com/arcgis/rest/services/ESRI_Imagery_World_2D/MapServer?f=json&pretty=true"
rlayer = QgsRasterLayer(path,"raster")
if vlayer.isValid():
    print("Valid")
else:
    print("Invalid")

cost = dict()

sys.path.append('C:/OSGeo4W64/apps/qgis/python/plugins') # Folder where Processing is located
from processing.core.Processing import Processing
Processing.initialize()
QgsApplication.processingRegistry().addProvider(QgsNativeAlgorithms())
print("Processing initiated")
from processing.tools import *
import processing

for feature in vlayer.getFeatures():
    if 'Neuro' in feature["Hospital_speciality"]:
        print(feature["Hospital_name"])
        lat = feature["Location-Latitude"]
        long = feature["Location-Longitude"]
        #print(lat, long)
        dest = long+","+lat+" [EPSG:4326]"
        print(dest)
        result = general.run("native:shortestpathpointtopoint", {'INPUT':'C:/Users/acer/Downloads/hosp_road.shp','STRATEGY':0,'DIRECTION_FIELD':None,'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'','DEFAULT_DIRECTION':2,'SPEED_FIELD':None,'DEFAULT_SPEED':50,'TOLERANCE':0,'START_POINT':'73.02217460971042,19.04214447607201 [EPSG:4326]','END_POINT':dest,'OUTPUT':'memory:'})
        print(result['TRAVEL_COST'])
        cost[dest] = result['TRAVEL_COST']
        min_cost = min(cost.keys(), key=(lambda k: cost[k]))

print(min_cost)
result = general.run("native:shortestpathpointtopoint", {'INPUT':'C:/Users/acer/Downloads/hosp_road.shp','STRATEGY':0,'DIRECTION_FIELD':None,'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'','DEFAULT_DIRECTION':2,'SPEED_FIELD':None,'DEFAULT_SPEED':50,'TOLERANCE':0,'START_POINT':'73.02217460971042,19.04214447607201 [EPSG:4326]','END_POINT':min_cost,'OUTPUT':'memory:'})
#print(result['OUTPUT'])
#QgsProject.instance().addMapLayers([result['OUTPUT']])

result['OUTPUT'].renderer().symbol().setWidth(1.0)
result['OUTPUT'].renderer().symbol().setColor(QColor("red"))
result['OUTPUT'].triggerRepaint()

canvas = QgsMapCanvas()
canvas.setCanvasColor(Qt.white)
canvas.enableAntiAliasing(True)
canvas.setExtent(result['OUTPUT'].extent())
canvas.setLayers([vlayer,result['OUTPUT'],rlayer])
canvas.freeze(True)
canvas.show()

exitcode = app.exec_()
app.exitQgis()
sys.exit(exitcode)
