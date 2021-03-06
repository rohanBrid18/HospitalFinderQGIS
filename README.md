# HospitalFinderQGIS
An application that finds hospitals near you

This application takes user's current device location and finds the shortest route to the nearest hospital according to the user's preferences.

The application works only in a particular locality. The hospital dataset and the road network shapefile used in this case is for Navi Mumbai, India. To use this application in any other locality, you need to collect the hospital dataset and create a road network shapefile for the corresponding locality.

## Getting started
The application is developed in an independent python script using QGIS python API (PyQGIS). To run the application, you will need to download and install QGIS simulator from https://qgis.org/en/site/forusers/download.html.

To enable python development using QGIS, you need to set the environment path for OSGeo4W.
Follow this link for assistance - https://www.youtube.com/watch?v=Chq9fTRKsHk.
Once you have set the environment variables, you can run the code (root.py) in OSGeo4W shell.
