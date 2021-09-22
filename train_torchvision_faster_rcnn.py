from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class IkomiaPlugin(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        from train_torchvision_faster_rcnn.train_torchvision_faster_rcnn_process import TrainFasterRcnnFactory
        # Instantiate process object
        return TrainFasterRcnnFactory()

    def getWidgetFactory(self):
        from train_torchvision_faster_rcnn.train_torchvision_faster_rcnn_widget import TrainFasterRcnnWidgetFactory
        # Instantiate associated widget object
        return TrainFasterRcnnWidgetFactory()
