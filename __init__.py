from .Loader import Loader


loader = Loader()

loader.setup_rembg()
loader.setup_paths()

NODE_CLASS_MAPPINGS = loader.get_modules()
