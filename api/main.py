from fastapi import FastAPI
from api.routes import model
from api.logging import get_logger
from api.controller import ModelController
from contextlib import asynccontextmanager
from api.utils.config import get_settings
from api.utils.redis_client import get_redis_client

logger = get_logger(__name__)
setting = get_settings()




@asynccontextmanager
async def lifespan(app: FastAPI):
    # This check runs on startup
    if not setting.MODEL_PATH.exists():
        error_msg = f"Model not found at {setting.MODEL_PATH}. Please run `python download_model.py` to download the model before starting the application."
        logger.critical(error_msg)
        raise FileNotFoundError(error_msg)

    logger.info("Loading the model ...")
    app.state.llm_model = ModelController().loading_model()
    app.state.redis_client = get_redis_client()
    yield
    logger.info("Unloading model ...")
    app.state.llm_model = None
    if app.state.redis_client:
        app.state.redis_client.close()


app = FastAPI(title="LLM GitHub Repo Reviewer", lifespan=lifespan)


app.include_router(model.model_router)


