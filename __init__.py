from .Loader import Loader

loader = Loader()

loader.setup_config()
loader.setup_timestamp()
loader.check_updates()
loader.setup_rembg()
loader.setup_paths()
loader.setup_override()

NODE_CLASS_MAPPINGS = loader.get_modules()
