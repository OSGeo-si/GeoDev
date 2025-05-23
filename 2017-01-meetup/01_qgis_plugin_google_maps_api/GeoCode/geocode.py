# -*- coding: utf-8 -*-
"""
/***************************************************************************
 GeoCode
                                 A QGIS plugin
 Geocoding using Google maps API
                              -------------------
        begin                : 2017-09-17
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Nejc Dougan
        email                : nejc.dougan@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.gui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources

# Import the code for the DockWidget
from geocode_dockwidget import GeoCodeDockWidget
import os.path
import requests
import json



class GeoCode:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'GeoCode_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&GeoCode')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'GeoCode')
        self.toolbar.setObjectName(u'GeoCode')

        #print "** INITIALIZING GeoCode"

        self.pluginIsActive = False
        self.dockwidget = None

        self.locationAddress = []
        self.locationCoo = []

        self.googleApiUrl = 'https://maps.googleapis.com/maps/api/geocode/'
        self.googleApiKey = 'AIzaSyBypRKpFU3eF85J311C8Y8GhsXEuSxja7E'
        self.format = 'json'


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('GeoCode', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToWebMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/GeoCode/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'GeoCode'),
            callback=self.run,
            parent=self.iface.mainWindow())

    #--------------------------------------------------------------------------

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        #print "** CLOSING GeoCode"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD GeoCode"

        for action in self.actions:
            self.iface.removePluginWebMenu(
                self.tr(u'&GeoCode'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


###################################################
    def loadFile(self):
        with open(QFileDialog.getOpenFileName(self.dockwidget, "Select file")) as f:
            for line in f:
                self.locationAddress.append(line)

        self.dockwidget.textPreview.setText(''.join(str(e) for e in self.locationAddress))

    def getGeoCode(self, address):
        request = self.googleApiUrl + self.format + '?key=' + self.googleApiKey + '&address=' + address
        print request
        try:
            return requests.get(request)
        except requests.ConnectionError as error:
            self.iface.messageBar().pushMessage("Connection error: ",
                                                'Can not access serivce! Check your intrenet connection.',
                                                level=QgsMessageBar.CRITICAL)
            return False

    def geocode(self):
        vl = QgsVectorLayer("Point", "geocoding_points", "memory")
        pr = vl.dataProvider()
        vl.startEditing()

        # add fields
        pr.addAttributes([QgsField("formatted_address", QVariant.String),
                          QgsField("route", QVariant.String),
                          QgsField("street_number", QVariant.String),
                          QgsField("administrative_area_level_1", QVariant.String),
                          QgsField("postal_code", QVariant.String),
                          QgsField("postal_town", QVariant.String),
                          QgsField("country", QVariant.String)])

        attributes = ["route", "street_number", "administrative_area_level_1",
                      "postal_code", "postal_town", "country", "formatted_address"]

        vl.updateFields()

        for address in self.locationAddress:
            response = self.getGeoCode(address.replace(" ", "+"))
            # print response
            # print response.content
            if response:
                content = json.loads(response.content)
                for result in content['results']:
                    # print result
                    # print result['geometry']['location']['lng']
                    # print result['formatted_address']
                    fet = QgsFeature()
                    fet.setGeometry(QgsGeometry.fromPoint(QgsPoint(result['geometry']['location']['lng'],
                                                                   result['geometry']['location']['lat'])))

                    #Add attributes
                    values = [result['formatted_address']]
                    for attribute in attributes:
                        for component in result['address_components']:
                            if component['types'][0] == attribute:
                                values.append(component['long_name'])

                    fet.setAttributes(values)
                    pr.addFeatures([fet])

        vl.commitChanges()
        QgsMapLayerRegistry.instance().addMapLayer(vl)


        #Add labels!
        palyr = QgsPalLayerSettings()
        palyr.readFromLayer(vl)
        palyr.enabled = True
        palyr.fieldName = 'formatted_address'
        palyr.setDataDefinedProperty(QgsPalLayerSettings.Size, True, True, '20', '')
        palyr.writeToLayer(vl)


    #--------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = GeoCodeDockWidget()

                #Bind buttons to actions
                self.dockwidget.pushButtonLoad.clicked.connect(self.loadFile)
                self.dockwidget.pushButtonGeoCode.clicked.connect(self.geocode)



            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()

