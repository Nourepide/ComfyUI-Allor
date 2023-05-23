import os
from typing import List

import numpy as np
import pooch
from PIL import Image
from PIL.Image import Image as PILImage

from .CustomSession import CustomBaseSession


class IsnetisSession(CustomBaseSession):
    def predict(self, img: PILImage, *args, **kwargs) -> List[PILImage]:
        ort_outs = self.inner_session.run(
            None,
            self.normalize(img, (0.8, 0.8, 0.8), (1.0, 1.0, 1.0), (1024, 1024)),
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
        pooch.retrieve(
            "https://huggingface.co/skytnt/anime-seg/resolve/main/isnetis.onnx",
            "SHA256:f15622d853e8260172812b657053460e20806f04b9e05147d49af7bed31a6e99",
            fname=fname,
            path=cls.u2net_home(),
            progressbar=True,
        )

        return os.path.join(cls.u2net_home(), fname)

    @classmethod
    def name(cls, *args, **kwargs):
        return "isnetis"
