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
                "SHA256:647990c98c409fbf6a72cd2a2db5fe19d2e4b15a3a436ef0302be0582458b63e",
                fname=f"export_onnx.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/onnx/modnet_onnx.py",
                "SHA256:0502cad1b7ab0bf2f866179960454c1e63df096390db05e93cb40145dbc26e1f",
                fname=f"modnet_onnx.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/src/models/backbones/__init__.py",
                "SHA256:28a5fb95f7dcf9e365edbf42c6d2e8ea0ca4839e51fd7f11bd0547d2359fcd96",
                fname=f"__init__.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/src/models/backbones"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/src/models/backbones/mobilenetv2.py",
                "SHA256:e3cc8ad6a9933ba18a17a62d5f887c64e0721240871ea8b48742fb9a8a2c3199",
                fname=f"mobilenetv2.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/src/models/backbones"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://raw.githubusercontent.com/ZHKKKe/MODNet/master/src/models/backbones/wrapper.py",
                "SHA256:41197be7eb96b8a60dc034b55d8c9340dd682a41441dcf2ce67238955dfa5607",
                fname=f"wrapper.py",
                path=os.path.join(cls.u2net_home(), "modnet-p/src/models/backbones"),
                progressbar=True,
            )

            pooch.retrieve(
                "https://storage.openvinotoolkit.org/repositories/open_model_zoo/public/2022.2/modnet-photographic-portrait-matting/modnet_photographic_portrait_matting.ckpt",
                "SHA256:7c22235f0925deba15d4d63e53afcb654c47055bbcd98f56e393ab2584007ed8",
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
