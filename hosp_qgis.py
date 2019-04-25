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
from qgis.PyQt.QtWidgets import QAction, QMainWindow

#   Instantiate the QGIS Application
GUIEnabled = False
app = QgsApplication([], GUIEnabled)
#   Update prefix path
app.setPrefixPath("C:/OSGeo4W64/apps/qgis", True)
app.initQgis()

#User inputs
spc = input("Select Hospital Speciality\n1. Cardiology\n2. Gynaecology\n3. Neurology\n4. Orthopedic Surgeon\n5. Physiology\n6. Surgeon\n7. Allergist\n8. Children's Hospital\n")
typ = input("Select Hospital type\n1. Private\n2. Government\n3. Trust\n4. All\n")
flag = 0

spcl = {'1': 'cardio', '2': 'Gyneco', '3':'Neuro', '4':'Orthopedic', '5':'Physio', '6':'Surgeon', '7':'allergist', '8':'Children_Hospital'}
typ1 = {'1':'private', '2': 'government', '3':'trust', '4':'all'}

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
print("Processing initiated\n")
from processing.tools import *
import processing


class MyWnd(QMainWindow):
    def __init__(self, layer, src, dst):
        QMainWindow.__init__(self)

        self.canvas = QgsMapCanvas()
        self.canvas.setCanvasColor(Qt.white)

        self.canvas.setExtent(layer.extent())
        self.canvas.setLayers([layer,src,dst,rlayer])

        self.setCentralWidget(self.canvas)

        self.actionZoomIn = QAction("Zoom in", self)
        self.actionZoomOut = QAction("Zoom out", self)
        self.actionPan = QAction("Pan", self)

        self.actionZoomIn.setCheckable(True)
        self.actionZoomOut.setCheckable(True)
        self.actionPan.setCheckable(True)

        self.actionZoomIn.triggered.connect(self.zoomIn)
        self.actionZoomOut.triggered.connect(self.zoomOut)
        self.actionPan.triggered.connect(self.pan)

        self.toolbar = self.addToolBar("Canvas actions")
        self.toolbar.addAction(self.actionZoomIn)
        self.toolbar.addAction(self.actionZoomOut)
        self.toolbar.addAction(self.actionPan)

        # create the map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolPan.setAction(self.actionPan)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        self.toolZoomIn.setAction(self.actionZoomIn)
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
        self.toolZoomOut.setAction(self.actionZoomOut)

        self.pan()

    def zoomIn(self):
        self.canvas.setMapTool(self.toolZoomIn)

    def zoomOut(self):
        self.canvas.setMapTool(self.toolZoomOut)

    def pan(self):
        self.canvas.setMapTool(self.toolPan)


for feature in vlayer.getFeatures():
    if typ1[typ] == 'all':
        print(feature["Hospital_name"])
        lat = feature["Location-Latitude"]
        long = feature["Location-Longitude"]
        #print(lat, long)
        dest = long+","+lat+" [EPSG:4326]"
        print(dest)
        result = general.run("native:shortestpathpointtopoint", {'INPUT':'C:/Users/acer/Downloads/hosp_road.shp','STRATEGY':0,'DIRECTION_FIELD':None,'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'','DEFAULT_DIRECTION':2,'SPEED_FIELD':None,'DEFAULT_SPEED':50,'TOLERANCE':0,'START_POINT':'73.02217460971042,19.04214447607201 [EPSG:4326]','END_POINT':dest,'OUTPUT':'memory:'})
        print("Travel Cost:",result['TRAVEL_COST'],"\n")
        cost[dest,feature["Hospital_name"]] = result['TRAVEL_COST']
        flag += 1
    elif typ1[typ] in feature["Hospital_Type"] and spcl[spc] in feature["Hospital_speciality"]:
        print(feature["Hospital_name"])
        lat = feature["Location-Latitude"]
        long = feature["Location-Longitude"]
        #print(lat, long)
        dest = long+","+lat+" [EPSG:4326]"
        print(dest)
        result = general.run("native:shortestpathpointtopoint", {'INPUT':'C:/Users/acer/Downloads/hosp_road.shp','STRATEGY':0,'DIRECTION_FIELD':None,'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'','DEFAULT_DIRECTION':2,'SPEED_FIELD':None,'DEFAULT_SPEED':50,'TOLERANCE':0,'START_POINT':'73.02217460971042,19.04214447607201 [EPSG:4326]','END_POINT':dest,'OUTPUT':'memory:'})
        print("Travel Cost:",result['TRAVEL_COST'],"\n")
        cost[dest,feature["Hospital_name"]] = result['TRAVEL_COST']
        flag += 1

if flag == 0:
    print("Sorry! No such hospital found.")
    quit()
        
min_cost = min(cost.keys(), key=(lambda k: cost[k]))

#print(min_cost)
dest = min_cost[0]
print("Nearest Hospital:",min_cost[1])
result = general.run("native:shortestpathpointtopoint", {'INPUT':'C:/Users/acer/Downloads/hosp_road.shp','STRATEGY':0,'DIRECTION_FIELD':None,'VALUE_FORWARD':'','VALUE_BACKWARD':'','VALUE_BOTH':'','DEFAULT_DIRECTION':2,'SPEED_FIELD':None,'DEFAULT_SPEED':50,'TOLERANCE':0,'START_POINT':'73.02217460971042,19.04214447607201 [EPSG:4326]','END_POINT':dest,'OUTPUT':'memory:'})

temp = dest.split(',')
temp[0] = float(temp[0])
temp1 = temp[1].split(' ')
temp1[0] = float(temp1[0])

source =  QgsVectorLayer('Point', 'points' , "memory")
pr = source.dataProvider() 
# add the first point
pt = QgsFeature()
point1 = QgsPointXY(73.02217460971042,19.04214447607201)
pt.setGeometry(QgsGeometry.fromPointXY(point1))
pr.addFeatures([pt])
# update extent of the layer
source.updateExtents()
source.renderer().symbol().setSize(3.0)
source.renderer().symbol().setColor(QColor("yellow"))
source.triggerRepaint()

destination =  QgsVectorLayer('Point', 'points' , "memory")
pr = destination.dataProvider()
# add the second point
pt = QgsFeature()
point2 = QgsPointXY(temp[0],temp1[0])
pt.setGeometry(QgsGeometry.fromPointXY(point2))
pr.addFeatures([pt])
# update extent
destination.updateExtents()
destination.renderer().symbol().setSize(3.0)
destination.renderer().symbol().setColor(QColor("red"))
destination.triggerRepaint()

#print(result['OUTPUT'])
#QgsProject.instance().addMapLayers([result['OUTPUT']])

result['OUTPUT'].renderer().symbol().setWidth(1.0)
result['OUTPUT'].renderer().symbol().setColor(QColor("blue"))
result['OUTPUT'].triggerRepaint()

w = MyWnd(result['OUTPUT'],source,destination)
w.show()

'''canvas = QgsMapCanvas()
canvas.setCanvasColor(Qt.white)
canvas.enableAntiAliasing(True)
canvas.setExtent(result['OUTPUT'].extent())
canvas.setLayers([vlayer,result['OUTPUT'],rlayer])
canvas.freeze(True)
canvas.show()'''

exitcode = app.exec_()
app.exitQgis()
sys.exit(exitcode)
