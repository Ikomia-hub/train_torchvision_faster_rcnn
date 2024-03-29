from ikomia import utils, core, dataprocess
from ikomia.core.task import TaskParam
from ikomia.dnn import dnntrain, datasetio
import os
import copy
from train_torchvision_faster_rcnn import faster_rcnn


# --------------------
# - Class to handle the process parameters
# - Inherits core.CProtocolTaskParam from Ikomia API
# --------------------
class TrainFasterRcnnParam(TaskParam):

    def __init__(self):
        TaskParam.__init__(self)
        # Place default value initialization here
        self.cfg["model_name"] = 'fasterRCNN'
        self.cfg["batch_size"] = 8
        self.cfg["classes"] = 2
        self.cfg["epochs"] = 15
        self.cfg["num_workers"] = 0
        self.cfg["input_size"] = 224
        self.cfg["momentum"] = 0.9
        self.cfg["learning_rate"] = 0.005
        self.cfg["weight_decay"] = 0.0005
        self.cfg["export_pth"] = True
        self.cfg["export_onnx"] = False
        self.cfg["output_folder"] = os.path.dirname(os.path.realpath(__file__)) + "/models/"

    def set_values(self, param_map):
        self.cfg["model_name"] = param_map["model_name"]
        self.cfg["batch_size"] = int(param_map["batch_size"])
        self.cfg["classes"] = int(param_map["classes"])
        self.cfg["epochs"] = int(param_map["epochs"])
        self.cfg["num_workers"] = int(param_map["num_workers"])
        self.cfg["input_size"] = int(param_map["input_size"])
        self.cfg["momentum"] = float(param_map["momentum"])
        self.cfg["learning_rate"] = float(param_map["learning_rate"])
        self.cfg["weight_decay"] = float(param_map["weight_decay"])
        self.cfg["export_pth"] = utils.strtobool(param_map["export_pth"])
        self.cfg["export_onnx"] = utils.strtobool(param_map["export_onnx"])
        self.cfg["output_folder"] = param_map["output_folder"]


# --------------------
# - Class which implements the process
# - Inherits core.CProtocolTask or derived from Ikomia API
# --------------------
class TrainFasterRcnn(dnntrain.TrainProcess):

    def __init__(self, name, param):
        dnntrain.TrainProcess.__init__(self, name, param)

        # Create parameters class
        if param is None:
            self.set_param_object(TrainFasterRcnnParam())
        else:
            self.set_param_object(copy.deepcopy(param))

        self.trainer = faster_rcnn.FasterRCNN(self.get_param_object())
        self.enable_tensorboard(False)

    def get_progress_steps(self):
        # Function returning the number of progress steps for this process
        # This is handled by the main progress bar of Ikomia application
        param = self.get_param_object()
        if param is not None:
            return param.cfg["epochs"]
        else:
            return 1

    def run(self):
        # Core function of your process

        # Get parameters :
        param = self.get_param_object()

        # Get dataset path from input
        dataset_input = self.get_input(0)
        param.cfg["classes"] = dataset_input.get_category_count()

        # Call begin_task_run for initialization
        self.begin_task_run()

        print("Starting training job...")
        self.trainer.launch(dataset_input, self.on_epoch_end)

        print("Training job finished.")

        # Call end_task_run to finalize process
        self.end_task_run()

    def on_epoch_end(self, metrics):
        # Step progress bar:
        self.emit_step_progress()
        # Log metrics
        self.log_metrics(metrics)

    def stop(self):
        super().stop()
        self.trainer.stop()


# --------------------
# - Factory class to build process object
# - Inherits dataprocess.CProcessFactory from Ikomia API
# --------------------
class TrainFasterRcnnFactory(dataprocess.CTaskFactory):

    def __init__(self):
        dataprocess.CTaskFactory.__init__(self)
        # Set process information as string here
        self.info.name = "train_torchvision_faster_rcnn"
        self.info.short_description = "Training process for Faster R-CNN convolutional network."
        self.info.authors = "Ikomia"
        self.info.version = "1.2.4"
        self.info.year = 2020
        self.info.license = "MIT License"
        self.info.repository = "https://github.com/Ikomia-hub/train_torchvision_faster_rcnn"
        self.info.original_repository = "https://github.com/pytorch/vision"
        # relative path -> as displayed in Ikomia application process tree
        self.info.path = "Plugins/Python/Detection"
        self.info.icon_path = "icons/pytorch-logo.png"
        self.info.keywords = "object,detection,instance,ResNet,pytorch,train"
        self.info.algo_type = core.AlgoType.TRAIN
        self.info.algo_tasks = "OBJECT_DETECTION"

    def create(self, param=None):
        # Create process object
        return TrainFasterRcnn(self.info.name, param)
