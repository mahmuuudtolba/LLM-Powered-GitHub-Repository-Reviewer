import anyio
from fastapi import Request
from api.exception import CustomException
from api.logging import get_logger
import tempfile
import os
import git



INCLUDE_EXTENSIONS = {".py", ".md", ".yml", ".yaml", ".txt"}
logger = get_logger(__name__)

class DataController:
     
    def repo_content(self , repo_url):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                        logger.info(f"Cloning repo {repo_url} into {tmpdir}")
                        git.Repo.clone_from(repo_url, tmpdir)

                        content = []
                        for root, _, files in os.walk(tmpdir):
                            for file in files:
                                if any(file.endswith(ext) for ext in INCLUDE_EXTENSIONS):
                                    file_path = os.path.join(root, file)
                                    try:
                                        with open(file_path, "r", encoding="utf-8") as f:
                                            file_content = f.read()
                                            content.append(f"\n\n### {file} ###\n{file_content}")
                                    except Exception as e:
                                        logger.warning(f" Skipping unreadable file: {file_path}: {e}")

                        combined = "\n".join(content)
                        logger.info(f"Extracted {len(content)} files from repo")
                        return combined if combined else "No content found"
            

        except Exception as e:
            logger.error(f"Failed to clone the repo: {e}")
            raise CustomException("Failed to clone the repo", e)