from .boot.Config import Config
from .boot.Update import Update
from .boot.Paths import Paths
from .boot.Override import Override
from .boot.Modules import Modules

config = Config().initiate()

Update(config).initiate()
Paths(config).initiate()
Override(config).initiate()

NODE_CLASS_MAPPINGS = Modules(config).initiate()
