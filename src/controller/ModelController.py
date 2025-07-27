from llama_cpp import Llama
from utils.config import get_settings
import os
setting = get_settings()


class ModelController:
     
    def get_full_prompt(self , repo_text):
        return f"""<bos><start_of_turn>user
                    You are a senior MLOps engineer. Review this entire GitHub project and provide 
                    detailed suggestions for improvement in structure, code quality, documentation, CI/CD, 
                    modularity, and best practices:
                    {repo_text}
                    <end_of_turn>
                    <start_of_turn>model

                    """
    
    def loading_model(self):
        return Llama(model_path=str(setting.MODEL_PATH), n_ctx=setting.MODEL_N_CTX, n_threads=setting.MODEL_N_THREADS)
        

    def generate_review_stream(self, llm: Llama, full_prompt: str):
        stream = llm.create_completion(
            full_prompt, max_tokens=setting.MODEL_MAXTOKEN, stream=True
        )
        return stream

