# -*- coding: utf-8 -*-


from widgets.shared.graphics import ImageFactory
from .powerarmorinfowidget import PowerArmorInfoWidget
from .powerarmorconditionwidget import PowerArmorConditionWidget
    
class Controller:
    
    def __init__(self, handle):
        self.mhandle = handle
        self.imageFactory = ImageFactory(handle.basepath)
        
    def createPowerArmorInfoWidget(self, parent):
        self.powerArmorInfoWidget = PowerArmorInfoWidget(self.mhandle, self, parent)
        return self.powerArmorInfoWidget
    
    def createPowerArmorConditionWidget(self, parent):
        self.powerArmorConditionWidget = PowerArmorConditionWidget(self.mhandle, self, parent)
        return self.powerArmorConditionWidget
