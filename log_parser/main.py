import uvicorn

from log_parser.configs.config import load_config, Config
from log_parser.handlers import metrics_handler, version_handler
from log_parser.application.middlewares import auth
from log_parser.data_parser import LogParser

from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from loguru import logger
from datetime import datetime
import sys
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    config: Config = load_config()
    logger.remove()
    app.state.config = config
    debug_flag = os.getenv("DEBUG", "").lower() in ("true", "1", "yes")
    log_level = "DEBUG" if debug_flag else "INFO"
    if config.logging.save_logs:
        log_name = datetime.now().strftime(config.logging.log_name)
        logger.add(
            config.logging.log_dir / log_name,
            level=log_level,
            rotation=config.logging.log_rotation_period,
        )
    else:
        logger.add(sys.stdout, level="DEBUG" if debug_flag else "INFO")
    middleware_deps = [
        Depends(auth(config.api.login, config.api.password)),
    ]
    nginx_file_path = os.getenv("NGINX_FILE_PATH", "log_parser/data/log.log")
    if not nginx_file_path:
        error = f"Nginx file path was not set as an environment variable!"
        logger.error(error)
        raise Exception(error)
    app.state.log_parser = LogParser(nginx_file_path, config.api.re_model_file_path)
    app.include_router(metrics_handler.router, dependencies=middleware_deps)
    app.include_router(version_handler.router)
    logger.info(f"--- Application start up completed ---")
    yield
    logger.info(f"--- Application has been shut down ---")


app = FastAPI(lifespan=lifespan)

if __name__ == "__main__":
    try:
        uvicorn.run(
            "main:app",
            host=os.getenv("API_HOST", "127.0.0.1"),
            port=int(os.getenv("API_PORT", "8040")),
        )
    except KeyboardInterrupt:
        logger.info(f"Application will be stopped")
