import anyio
from fastapi import Request
from src.api.exception import CustomException
from src.api.logging import get_logger
import tempfile
import os
import git



INCLUDE_EXTENSIONS = {".py", ".md", ".yml", ".yaml", ".txt"}
logger = get_logger(__name__)

class DataController:
     
    def get_repo_contents(self , repo_url):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                        logger.info(f"Cloning repo {repo_url} into {tmpdir}")
                        git.Repo.clone_from(repo_url, tmpdir)

                        repo_contents = []
                        for root, _, files in os.walk(tmpdir):
                            for file in files:
                                is_supported_extention = any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS)
                                if is_supported_extention :
                                    file_path = os.path.join(root, file)
                                    try:
                                        with open(file_path, "r", encoding="utf-8") as f:
                                            file_content = f.read()
                                            repo_contents.append(f"\n\n### {file} ###\n{file_content}")
                                    except Exception as e:
                                        logger.warning(f" Skipping unreadable file: {file_path}: {e}")

                        combined = "\n".join(repo_contents)
                        logger.info(f"Extracted {len(repo_contents)} files from repo")
                        return combined if combined else "No content found"
            

        except Exception as e:
            logger.error(f"Failed to clone the repo: {e}")
            raise CustomException("Failed to clone the repo", e)