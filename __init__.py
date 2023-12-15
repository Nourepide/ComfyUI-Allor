from .boot.Logger import Logger
from .boot.Backends import Backends
from .boot.Config import Config
from .boot.Update import Update
from .boot.Paths import Paths
from .boot.Override import Override
from .boot.Modules import Modules

logger = Logger()
config = Config(logger).initiate()
backends = Backends(logger).initiate()

Update(logger, config, backends).initiate()
Paths(logger, config, backends).initiate()
Override(logger, config, backends).initiate()

NODE_CLASS_MAPPINGS = Modules(logger, config, backends).initiate()
