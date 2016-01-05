# -*- coding: utf-8 -*-


import os
import math
from PyQt5 import QtWidgets, QtCore, uic
from pypipboy.types import eValueType
from .. import widgets
from pypipboy import inventoryutils


powerArmorPaperDollSlots = [
    'Body', # 0
    'leftleg', # 1
    'rightleg', # 2
    'leftarm', # 3
    'rightarm', # 4
    'torso', # 5
    'head', # 6
    'head',#7
    'head'#8
    ]
class PowerArmorInfoWidget(widgets.WidgetBase):
    _signalInfoUpdated = QtCore.pyqtSignal()
    
    def __init__(self, handle, controller, parent):
        super().__init__('Power Armor Info', parent)
        self.controller = controller
        self.widget = uic.loadUi(os.path.join(handle.basepath, 'ui', 'powerarmorinfowidget.ui'))
        self.setWidget(self.widget)
        self.pipPlayerInfo = None
        self._signalInfoUpdated.connect(self._slotInfoUpdated)
        self.paHP = {}
        for item in powerArmorPaperDollSlots:
            self.paHP[item + 'Max'] = 0



    def init(self, app, datamanager):
        super().init(app, datamanager)
        self.dataManager = datamanager
        self.dataManager.registerRootObjectListener(self._onPipRootObjectEvent)
        
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
                    itemTxt = item.child('text').value()

                    i = 0
                    paperDollLoc = None
                    for section in item.child('PaperdollSection').value():
                        if section.value():
                                self.paHP[powerArmorPaperDollSlots[i] + 'Cur'] = int(itemHealth[0])
                                self.paHP[powerArmorPaperDollSlots[i] + 'Max'] = int(itemHealth[1])
                                maxHP = self.paHP[powerArmorPaperDollSlots[i] + 'Max']
                                curHP = self.paHP[powerArmorPaperDollSlots[i] + 'Cur']
                                percentHP = (curHP*100/maxHP)
                                if itemTxt:
                                    self.widget.headItemLabel.setText(itemTxt)
                                self.setWidgetValues(powerArmorPaperDollSlots[i],percentHP, itemHealthTxt,itemTxt)
                                equipedPA.append(powerArmorPaperDollSlots[i])
                        i+=1
            for item in powerArmorPaperDollSlots:
                if (not item in equipedPA and (not item == 'Body')):
                    self.setWidgetValues(item,0, 'Empty',' ')

    def setWidgetValues(self, subwidget,value,text,itemName):
        methodToCall = getattr(self.widget,subwidget + 'Bar')
        methodToCall.setValue(value)
        methodToCall = getattr(self.widget,subwidget + 'Label')
        methodToCall.setText(text)
        methodToCall = getattr(self.widget,subwidget + 'ItemLabel')
        methodToCall.setText(itemName)


