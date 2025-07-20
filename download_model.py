from api.utils.config import get_settings
import os
import requests
from api.logging import get_logger
from api.exception import CustomException
import time


logger = get_logger(__name__)

setting = get_settings()


if not setting.MODEL_PATH.exists():
    # Ensure the parent directory exists before attempting to download.
    setting.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    try:
        logger.info(f"Downloading the model from {setting.MODEL_DOWNLOAD_URL} to {setting.MODEL_PATH}")

        url = setting.MODEL_DOWNLOAD_URL
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(setting.MODEL_PATH, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        logger.info(f"Model downloaded and saved to {setting.MODEL_PATH}")

    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise CustomException("Failed to download model", e)