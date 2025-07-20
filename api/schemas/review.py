from pydantic import BaseModel



class RepoInput(BaseModel):
    repo_url: str
    