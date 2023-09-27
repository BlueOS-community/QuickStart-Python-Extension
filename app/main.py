#!/usr/bin/env python3

from pathlib import Path
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
import aiohttp
from litestar import Litestar, get, MediaType
from litestar.controller import Controller
from litestar.datastructures import State

class CountController(Controller):
    def __init__(self, *args, **kwargs):
        self._temp_count = -1
        super().__init__(*args, **kwargs)

    @get("/", media_type=MediaType.HTML)
    def root() -> str:
        return Path('index.html').read_text()

    @get("/temp_count")
    def increment_temp_count(self) -> dict[str, int]:
        self._temp_count += 1
        return {"value": self._temp_count}

    @get("/persistent_count")
    async def increment_persistent_count(self, state: State) -> dict[str, int]:
        # read the existing persistent count value (from the BlueOS "Bag of Holding" service API)
        try:
            async with state.session.get(state.bag_url + '/get/quickstart-count') as response:
                value = int(await response.text())
        except Exception: # TODO: specifically except HTTP error 400
            value = 0
        value += 1
        # write the incremented value back out
        await self._session.post(state.bag_url + /set/quickstart-count, data=value) # convert to str/JSONResponse?
        return {"value": value}


if __name__ == '__main__':
    import logging
    from argparse import ArgumentParser

    parser = ArgumentParser
    parser.add_argument('--log_path', type=Path, default='/root/.config/logs/')
    parser.add_argument('--bag_url', default='http://host.docker.internal:9101')
    args = parser.parse_args()

    logging.basicConfig(
        format='%(asctime)s: %(message)s', level=logging.INFO
    )
    
    logger = logging.getLogger(__name__)
    # TODO: create file logger handler - ideally rotating

    #def set_state_on_startup(app: Litestar) -> None:
    #    app.state.bag_url = args.bag_url

    async with aiohttp.ClientSession() as session:
        app = Litestar(
            route_handlers=[CountController],
            state=State({'bag_url':args.bag_url, 'session':session}),
            #on_startup=[set_state_on_startup],
            lifespan=[AppSession]
        )
