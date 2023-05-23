from .Loader import Loader
from .modules import Utils, AlphaChanel, Clamp, ImageComposite, ImageContainer, ImageSegmentation, ImageText


loader = Loader()

loader.setup_rembg()
loader.setup_paths()

NODE_CLASS_MAPPINGS = loader.get_modules()
