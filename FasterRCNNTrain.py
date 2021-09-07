from ikomia import dataprocess


# --------------------
# - Interface class to integrate the process with Ikomia application
# - Inherits dataprocess.CPluginProcessInterface from Ikomia API
# --------------------
class FasterRCNNTrain(dataprocess.CPluginProcessInterface):

    def __init__(self):
        dataprocess.CPluginProcessInterface.__init__(self)

    def getProcessFactory(self):
        from FasterRCNNTrain.FasterRCNNTrain_process import FasterRCNNTrainProcessFactory
        # Instantiate process object
        return FasterRCNNTrainProcessFactory()

    def getWidgetFactory(self):
        from FasterRCNNTrain.FasterRCNNTrain_widget import FasterRCNNTrainWidgetFactory
        # Instantiate associated widget object
        return FasterRCNNTrainWidgetFactory()
