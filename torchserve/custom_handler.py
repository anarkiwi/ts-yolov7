import os
import sys
from collections import defaultdict
import torch
from torchvision import transforms
from ts.torch_handler.object_detector import ObjectDetector

sys.path.append("/root/yolov7")

from models.experimental import attempt_load
from utils.general import check_img_size, non_max_suppression

IMG_SIZE = 640


class YoloV7Handler(ObjectDetector):
    image_processing = transforms.Compose(
        [
            transforms.Resize(IMG_SIZE),
            transforms.CenterCrop(IMG_SIZE),
            transforms.ToTensor(),
        ]
    )

    def __init__(self):
        super().__init__()
        self.device = None
        self.model = None
        self.model_pt_patch = None
        self.imgsz = None
        self.conf_thres = 0.25
        self.iou_thres = 0.45
        self.agnostic_nms = False
        self.classes = None
        self.names = None
        self.initialized = False
        self.stride = 0

    def initialize(self, context):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("Yolov7Handler: using cuda")
        else:
            self.device = torch.device("cpu")
            print("Yolov7Handler: using cpu")

        properties = context.system_properties
        self.manifest = context.manifest
        model_dir = properties.get("model_dir")
        self.model_pt_path = None
        if "serializedFile" in self.manifest["model"]:
            serialized_file = self.manifest["model"]["serializedFile"]
            self.model_pt_path = os.path.join(model_dir, serialized_file)
        self.model = self._load_torchscript_model(self.model_pt_path)
        self.stride = int(self.model.stride.max())
        self.imgsz = check_img_size(IMG_SIZE, s=self.stride)
        if self.device.type != "cpu":
            self.model(
                torch.zeros(1, 3, self.imgsz, self.imgsz)
                .to(self.device)
                .type_as(next(self.model.parameters()))
            )  # run once
        self.names = (
            self.model.module.names
            if hasattr(self.model, "module")
            else self.model.names
        )
        self.initialized = True

    def _load_torchscript_model(self, model_pt_path):
        """Loads the PyTorch model and returns the NN model object.

        Args:
            model_pt_path (str): denotes the path of the model file.

        Returns:
            (NN Model Object) : Loads the model object.
        """
        # TODO: remove this method if https://github.com/pytorch/text/issues/1793 gets resolved
        model = attempt_load(model_pt_path, map_location=self.device)
        return model

    def postprocess(self, data):
        pred = non_max_suppression(
            data[0],
            self.conf_thres,
            self.iou_thres,
            classes=self.classes,
            agnostic=self.agnostic_nms,
        )
        result_dict = defaultdict(list)
        for det in pred:
            if len(det):
                for *xyxy_ref, conf, cls in reversed(det):
                    xyxy = torch.tensor(xyxy_ref).view(1, 4).tolist()[0]
                    result_dict[self.names[int(cls)]].append(
                        {"conf": conf.tolist(), "xyxy": xyxy}
                    )
        return [result_dict]
