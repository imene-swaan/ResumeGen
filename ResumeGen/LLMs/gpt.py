import logging
from pathlib import Path
from typing import List, Optional
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
import toml
import os
from tenacity import retry, wait_random_exponential, stop_after_attempt



def find_project_root(filename=None) -> str:
    """
    Find the root folder of the project.

    Args:
        filename (str): The name of the file to look for in the root folder.

    Returns:
        str: The path of the root folder.

    """
    # Get the path of the file that is being executed
    current_file_path = os.path.abspath(os.getcwd())

    # Navigate back until we either find a $filename file or there is no parent
    # directory left.
    root_folder = current_file_path
    while True:
        # Custom way to identify the project root folder
        if filename is not None:
            env_file_path = os.path.join(root_folder, filename)
            if os.path.isfile(env_file_path):
                break

        # Most common ways to identify a project root folder
        if os.path.isfile(os.path.join(root_folder, "pyproject.toml")) or os.path.isfile(
            os.path.join(root_folder, "config.toml")
        ):
            break

        parent_folder = os.path.dirname(root_folder)
        if parent_folder == root_folder:
            raise ValueError("Could not find the root folder of the project.")

        root_folder = parent_folder

    return root_folder

def find_closest(filename: str) -> str:
    """
    Find the closest file with the given name in the project root folder.

    Args:
        filename (str): The name of the file to look for in the root folder.

    Returns:
        str: The path of the file.
    """
    return os.path.join(find_project_root(filename), filename)

class CFGGpt(BaseModel):
    """
    Config for OpenAI GPT-3 API
    """

    temperature: float
    n: int
    stop: List[str]
    stream: bool


class Gpt(BaseModel):
    """
    GPT-3 Model
    """

    name: str
    description: str
    config: CFGGpt


class Config(BaseModel):
    """
    Config for MentorMingle
    """

    model: Gpt

    @classmethod
    def from_toml(cls, config_file: Path) -> "Config":
        """
        Load config from toml file

        Args:
            config_file (Path): Path to config file

        Returns:
            Config: Config object
        """
        return cls(**toml.load(config_file))


load_dotenv()
logger = logging.getLogger(__name__)

class ChatHandler:
    """Handler for chat with GPT-3"""

    def __init__(
        self
    ):
        """Initialize the chat handler"""

        self.client = OpenAI(
            api_key= os.environ.get("OPENAI_KEY")
        )

        # Load config
        self.model = Config.from_toml(Path(find_closest("config.toml"))).model

    

    @retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
    def chat_completion_request(
        self,
        intro_session: List[dict],
        functions: Optional[List[dict]] = None,
        function_call: Optional[dict] = None,
        ):
        try:
            response = self.client.chat.completions.create(
                model=self.model.name,
                messages=intro_session,
                functions=functions,
                function_call=function_call,
                **self.model.config.model_dump(),
            )

            return self._Response(response, function_call)
        except Exception as e:
            raise Exception(f"Error in chat completion request: {e}")

   

    def _Response(self, response, function_call) -> str:
        """
        Generate response

        Args:
            response (str): Response from GPT-3

        Returns:
            str: Response
        """
        if function_call is None:
            return response.choices[0].message.content
        return response.choices[0].message.function_call.arguments

