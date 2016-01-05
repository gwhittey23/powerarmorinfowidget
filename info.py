
from widgets import widgets

from .controller import Controller

class ModuleInfo(widgets.ModuleInfoBase):
    
    LABEL = 'powerarmorinfo'
    NAME = 'Power Armor Info'

    @staticmethod
    def createWidgets(handle, parent):
        controller = Controller(handle)
        infoWidget = controller.createPowerArmorInfoWidget(parent)
        conditionWidget = controller.createPowerArmorConditionWidget(parent)
        return [infoWidget, conditionWidget]
