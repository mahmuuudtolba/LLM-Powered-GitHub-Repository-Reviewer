import anyio
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse
from llama_cpp import Llama
from api.logging import get_logger
from api.exception import CustomException
from api.schemas import RepoInput
import time
from api.controller import DataController, ModelController

model_router = APIRouter(prefix="/model", tags=["Model"])
logger = get_logger(__name__)


@model_router.get("/health-check")
async def health_check():
    """
    A simple endpoint to check if the server is responsive.
    """
    logger.info("Health check endpoint was called.")
    return {"status": "ok", "message": "Server is responsive."}


@model_router.post("/review")
async def test_model(repo_url : RepoInput , request : Request):
    
    redis_client = request.app.state.redis_client
    if redis_client:
        cached_review = redis_client.get(repo_url.repo_url)
        if cached_review:
            logger.info(f"Cache hit for {repo_url.repo_url}")
            async def stream_cached_review():
                yield cached_review
            return StreamingResponse(stream_cached_review(), media_type="text/event-stream")

    logger.info("Start reviewing... ")

    try:

        data_controller = DataController()
        model_controller = ModelController()

        content = await anyio.to_thread.run_sync(data_controller.repo_content , repo_url.repo_url)
        full_prompt = model_controller.get_full_prompt(content)

        logger.info("Loading the model")


        if hasattr(request.app.state, "llm_model") and request.app.state.llm_model:
            llm = request.app.state.llm_model
        
        logger.info(f"sending to gemma ..")

        async def stream_llm():
            stream = await anyio.to_thread.run_sync(
                lambda: model_controller.generate_review_stream(llm, full_prompt)
            )
            full_review = ""
            for chunk in stream:
                if "choices" in chunk and len(chunk["choices"]) > 0:
                    text = chunk["choices"][0]["text"]
                    full_review += text
                    yield text
            
            if redis_client:
                logger.info(f"Caching review for {repo_url.repo_url}")
                redis_client.set(repo_url.repo_url, full_review)
        
        logger.info("LLM response received")
        return StreamingResponse(stream_llm(), media_type="text/event-stream")

    except Exception as e:
        logger.error(f"Github review failed")
        raise CustomException("Github review failed", e)