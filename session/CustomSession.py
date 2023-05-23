import os
from typing import List

import numpy as np
import onnxruntime as ort
from PIL import Image
from PIL.Image import Image as PILImage
from rembg.sessions import BaseSession


class CustomBaseSession(BaseSession):
    def __init__(self, model_name: str):
        sess_opts = ort.SessionOptions()

        if "OMP_NUM_THREADS" in os.environ:
            sess_opts.inter_op_num_threads = int(os.environ["OMP_NUM_THREADS"])

        super().__init__(model_name, sess_opts)


class CustomSessionContainer:
    def __init__(self, mean_x, mean_y, mean_z, std_x, std_y, std_z, width, height) -> None:
        self.mean_x = mean_x
        self.mean_y = mean_y
        self.mean_z = mean_z
        self.std_x = std_x
        self.std_y = std_y
        self.std_z = std_z
        self.width = width
        self.height = height


class CustomAbstractSession(CustomBaseSession, CustomSessionContainer):
    def predict(self, img: PILImage, *args, **kwargs) -> List[PILImage]:
        ort_outs = self.inner_session.run(
            None,
            self.normalize(
                img,
                (self.mean_x, self.mean_y, self.mean_z),
                (self.std_x, self.std_y, self.std_z),
                (self.width, self.height)
            ),
        )

        pred = ort_outs[0][:, 0, :, :]

        ma = np.max(pred)
        mi = np.min(pred)

        pred = (pred - mi) / (ma - mi)
        pred = np.squeeze(pred)

        mask = Image.fromarray((pred * 255).astype("uint8"), mode="L")
        mask = mask.resize(img.size, Image.LANCZOS)

        return [mask]

    @classmethod
    def download_models(cls, *args, **kwargs):
        return os.path.join(cls.u2net_home(), f"{cls.name()}")

    def from_container(self, container: CustomSessionContainer):
        self.mean_x = container.mean_x
        self.mean_y = container.mean_y
        self.mean_z = container.mean_z
        self.std_x = container.std_x
        self.std_y = container.std_y
        self.std_z = container.std_z
        self.width = container.width
        self.height = container.height

        return self
