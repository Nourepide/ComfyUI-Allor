import os
import shutil
import subprocess
import sys
from typing import List

import numpy as np
import pooch
from PIL import Image
from PIL.Image import Image as PILImage

from .CustomSession import CustomBaseSession


class ModnetPhotographicSession(CustomBaseSession):
    def predict(self, img: PILImage, *args, **kwargs) -> List[PILImage]:
        ort_outs = self.inner_session.run(
            None,
            self.normalize(img, (0.5, 0.5, 0.5), (1.0, 1.0, 1.0), (512, 512)),
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
        fname = f"{cls.name()}.onnx"

        if not os.path.exists(os.path.join(cls.u2net_home(), fname)):
            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/onnx/export_onnx.py",
                known_hash=None,
                fname=f"export_onnx.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/onnx/modnet_onnx.py",
                known_hash=None,
                fname=f"modnet_onnx.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/src/models/backbones/__init__.py",
                known_hash=None,
                fname=f"__init__.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/src/models/backbones"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/src/models/backbones/mobilenetv2.py",
                known_hash=None,
                fname=f"mobilenetv2.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/src/models/backbones"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/src/models/backbones/wrapper.py",
                known_hash=None,
                fname=f"wrapper.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/src/models/backbones"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://storage.openvinotoolkit.org/repositories/open_model_zoo/public/2022.2/modnet-photographic-portrait-matting/modnet_photographic_portrait_matting.ckpt",
                known_hash=None,
                fname=f"modnet_photographic_portrait_matting.ckpt",
                path=os.path.join(cls.u2net_home(), "modnet-p/"),
                progressbar=True,
            )

            replace_line(
                os.path.join(cls.u2net_home(), "modnet-p/export_onnx.py"),
                "from . import modnet_onnx",
                "import modnet_onnx"
            )

            subprocess.run([
                sys.executable,
                os.path.join(cls.u2net_home(), "modnet-p/export_onnx.py"),
                "--ckpt-path=" + os.path.join(cls.u2net_home(), "modnet-p/modnet_photographic_portrait_matting.ckpt"),
                "--output-path=" + os.path.join(cls.u2net_home(), "modnet-p/../modnet-p.onnx"),
            ])

            shutil.rmtree(os.path.join(cls.u2net_home(), "modnet-p/"))

        return os.path.join(cls.u2net_home(), fname)

    @classmethod
    def name(cls, *args, **kwargs):
        return "modnet-p"


def replace_line(path: str, old: str, new: str):
    with open(path, "r", encoding="utf-8") as file:
        data = file.readlines()

    for i in range(len(data)):
        if data[i].__contains__(old):
            data[i] = data[i].replace(old, new)

    with open(path, "w", encoding="utf-8") as file:
        file.writelines(data)
