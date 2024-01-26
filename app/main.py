#!/usr/bin/env python3

import requests
import logging.handlers
from pathlib import Path
from litestar import Litestar, get, MediaType
from litestar.controller import Controller
from litestar.datastructures import State
from litestar.logging import LoggingConfig
from litestar.static_files.config import StaticFilesConfig

class CountController(Controller):
    COUNT_VAR = 'quickstart_backend_perm_count'
    def __init__(self, *args, **kwargs):
        self._temp_count = 0
        super().__init__(*args, **kwargs)

    @get("/temp_count", sync_to_thread=False)
    def increment_temp_count(self) -> dict[str, int]:
        self._temp_count += 1
        return {"value": self._temp_count}

    @get("/persistent_count", sync_to_thread=True)
    def increment_persistent_count(self, state: State) -> dict[str, int]:
        # read the existing persistent count value (from the BlueOS "Bag of Holding" service API)
        try:
            response = requests.get(f'{state.bag_url}/get/{self.COUNT_VAR}')
            response.raise_for_status()
            value = response.json()['value']
        except Exception as e:  # TODO: specifically except HTTP error 400 (using response.status_code?)
            value = 0
        value += 1
        # write the incremented value back out
        output = {'value': value}
        requests.post(f'{state.bag_url}/set/{self.COUNT_VAR}', json=output)
        return output

logging_config = LoggingConfig(
    loggers={
        __name__: dict(
            level='INFO',
            handlers=['queue_listener'],
        )
    },
)

log_dir = Path('/app/logs')
log_dir.mkdir(parents=True, exist_ok=True)
fh = logging.handlers.RotatingFileHandler(log_dir / 'lumber.log', maxBytes=2**16, backupCount=1)

app = Litestar(
    route_handlers=[CountController],
    state=State({'bag_url':'http://host.docker.internal/bag/v1.0'}),
    static_files_config=[
        StaticFilesConfig(directories=['app/static'], path='/', html_mode=True)
    ],
    logging_config=logging_config,
)

app.logger.addHandler(fh)
