# -*- coding: utf-8 -*-


import datetime
import os
from PyQt5 import QtWidgets, QtGui, QtCore, uic
from pypipboy.types import eValueType
from pypipboy import inventoryutils
from widgets import widgets

powerArmorPaperDollSlots = [
    'None', # 0
    'leftleg', # 1
    'rightleg', # 2
    'leftarm', # 3
    'rightarm', # 4
    'torso', # 5
    'head', # 6
    'head',#7
    'head'#8
    ]

paCords = {
    'head':     {'x': 35, 'y': 35},
    'torso':    {'x': 68, 'y': 68},
    'leftarm':  {'x': 35, 'y': 92},
    'leftleg':  {'x': 40, 'y': 98},
    'rightarm': {'x': 35, 'y': 92},
    'rightleg': {'x': 40, 'y': 98}
}

class PowerArmorConditionWidget(widgets.WidgetBase):
    _signalInfoUpdated = QtCore.pyqtSignal()
    
    def __init__(self, handle, controller, parent):
        super().__init__('Power Armor Condition', parent)
        self.controller = controller
        self.imageFactory = controller.imageFactory
        self.widget = uic.loadUi(os.path.join(handle.basepath, 'ui', 'powerarmorconditionwidget.ui'))
        self.setWidget(self.widget)
        self.pipStats = None
        self.bodyFlags = 0
        self.headerFlags = 0
        self._signalInfoUpdated.connect(self._slotInfoUpdated)
        self.paHP = {}
        self.powerArmorItemsSettings = {}
        for item in powerArmorPaperDollSlots:
            self.paHP[item + 'Max'] = 0


    def init(self, app, datamanager):
        super().init(app, datamanager)
        self.statsColor = QtGui.QColor.fromRgb(255,186,49)
        self.dataManager = datamanager
        self.dataManager.registerRootObjectListener(self._onPipRootObjectEvent)

        self.statsView = self.widget.graphicsView
        self.statsScene = QtWidgets.QGraphicsScene()
        self.statsScene.setBackgroundBrush(QtGui.QBrush(QtGui.QColor.fromRgb(0,0,0)))
        self.statsView.setScene(self.statsScene)

        """
        Make Paper Doll for Power Armor starting with empty shell
        """
        #head
        self.pa_headFullFilePath =  os.path.join('res', 'pa_head_empty.svg')
        headPixmap = self.imageFactory.getPixmap(self.pa_headFullFilePath, width=35,height=35, color=self.statsColor)
        self.pa_headItem = self.statsScene.addPixmap(headPixmap)
        self.pa_headItem.setPos(-headPixmap.width()/2, 0)

        #torso
        self.pa_torsoFullFilePath =  os.path.join('res', 'pa_torso_empty.svg')
        torsoPixmap = self.imageFactory.getPixmap(self.pa_torsoFullFilePath, width=68, height=68, color=self.statsColor)
        self.pa_torsoItem = self.statsScene.addPixmap(torsoPixmap)
        self.pa_torsoItem.setPos(-torsoPixmap.width()/2, 32)

        #leftarm
        self.pa_leftarmFullFilePath =  os.path.join('res', 'pa_leftarm_empty.svg')
        leftarmPixmap = self.imageFactory.getPixmap(self.pa_leftarmFullFilePath, width=35, height=92, color=self.statsColor)
        self.pa_leftarmItem = self.statsScene.addPixmap(leftarmPixmap)
        self.pa_leftarmItem.setPos((-leftarmPixmap.width()/2)-44, 35)

        #leftleg
        self.pa_leftlegFullFilePath =  os.path.join('res', 'pa_leftleg_empty.svg')
        leftlegPixmap = self.imageFactory.getPixmap(self.pa_leftlegFullFilePath, width=40, height=98, color=self.statsColor)
        self.pa_leftlegItem = self.statsScene.addPixmap(leftlegPixmap)
        self.pa_leftlegItem.setPos((-leftlegPixmap.width()/2)-22, 98)

        #rightarm
        self.pa_rightarmFullFilePath =  os.path.join('res', 'pa_rightarm_empty.svg')
        rightarmPixmap = self.imageFactory.getPixmap(self.pa_rightarmFullFilePath, width=35, height=92, color=self.statsColor)
        self.pa_rightarmItem = self.statsScene.addPixmap(rightarmPixmap)
        self.pa_rightarmItem.setPos((-rightarmPixmap.width()/2)+44, 35)

        #rightleg
        self.pa_rightlegFullFilePath =  os.path.join('res', 'pa_rightleg_empty.svg')
        rightlegPixmap = self.imageFactory.getPixmap(self.pa_rightlegFullFilePath, width=40, height=98, color=self.statsColor)
        self.pa_rightlegItem = self.statsScene.addPixmap(rightlegPixmap)
        self.pa_rightlegItem.setPos((-rightlegPixmap.width()/2)+22, 98)



    def _onPipRootObjectEvent(self, rootObject):
        self.pipInventoryInfo = rootObject.child('Inventory')
        if self.pipInventoryInfo:
            self.pipInventoryInfo.registerValueUpdatedListener(self._onPipInventoryInfoUpdate, 1)
        self._signalInfoUpdated.emit()


    def _onPipInventoryInfoUpdate(self, caller, value, pathObjs):
        self._signalInfoUpdated.emit()

    @QtCore.pyqtSlot()
    def _slotInfoUpdated(self):
        self.getPowerArmorItems()

    def getPowerArmorItems(self):
        equipedPA = []
        for item in powerArmorPaperDollSlots:
            self.paHP[item + 'Cur'] = 0

        if (self.pipInventoryInfo):
            def _filterFunc(item):
                return inventoryutils.itemHasAnyFilterCategory(item, inventoryutils.eItemFilterCategory.Apparel)

            power_armor = inventoryutils.inventoryGetItems(self.pipInventoryInfo, _filterFunc)
            for item in power_armor:

                if (item.child('isPowerArmorItem').value() and (item.child('equipState').value() == 1)):
                    itemHealthTxt = inventoryutils.itemFindItemCardInfoValue(item, '$health')
                    itemHealth = itemHealthTxt.split('/')
                    i = 0
                    paperDollLoc = None
                    for section in item.child('PaperdollSection').value():
                        if section.value():
                                self.paHP[powerArmorPaperDollSlots[i] + 'Cur'] = int(itemHealth[0])
                                self.paHP[powerArmorPaperDollSlots[i] + 'Max'] = int(itemHealth[1])
                                maxHP = self.paHP[powerArmorPaperDollSlots[i] + 'Max']
                                curHP = self.paHP[powerArmorPaperDollSlots[i] + 'Cur']
                                percentHP = (curHP*100/maxHP)
                                paSlot = powerArmorPaperDollSlots[i]
                                self.setPowerArmorCondition(paSlot,percentHP, paCords[paSlot]['x'],paCords[paSlot]['y'])
                                equipedPA.append(powerArmorPaperDollSlots[i])
                        i+=1
            for item in powerArmorPaperDollSlots:
                if (not item in equipedPA and (not item == 'None')):
                    paSlot = item
                    self.setPowerArmorCondition(paSlot,'Empty', paCords[paSlot]['x'],paCords[paSlot]['y'])

    def setPowerArmorCondition(self,paSlot,percentHP,slotWidth,slotHeight):
        if percentHP == 'Empty':
            stateFile = 'pa_' + paSlot + '_empty.svg'
            self.statsColor = QtGui.QColor.fromRgb(255, 186, 49)
        else:
            stateFile = 'pa_' + paSlot + '_filled.svg'
            if (percentHP >= 50):
                self.statsColor = QtGui.QColor.fromRgb(15, 186, 49)
            elif (percentHP < 50) and (percentHP > 25) :
                self.statsColor = QtGui.QColor.fromRgb(255, 186, 49)
            else:
                self.statsColor = QtGui.QColor.fromRgb(255, 0, 0)
        stateFilePath =  os.path.join('res', stateFile)
        paPixmap = self.imageFactory.getPixmap(stateFilePath, width=slotWidth, height=slotHeight, color=self.statsColor)
        methodToCall = getattr(self, 'pa_' + paSlot + 'Item')
        methodToCall.setPixmap(paPixmap)

