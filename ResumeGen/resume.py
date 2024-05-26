import jsonschema.exceptions
from ResumeGen.LLMs.gpt import ChatHandler
from jinja2 import Environment, FileSystemLoader
import json
from pathlib import Path
from typing import Dict, Union, Optional, Tuple
import jsonschema
from jsonschema import validate

class ResumeGPT:
    def __init__(
            self,
            templates: Union[Path, str] = "templates",
            ):
        
        self.template_path = f"{templates}/resume_template.tex.j2"

        with open(f"{templates}/FunctionSpec.json") as f:
            self.setResumeFunctionSpec = json.load(f)
        

        with open(f"{templates}/schema.json") as f:
            self.schema = json.load(f)


       

    def _validate_json(self, data) -> Tuple[bool, Optional[str]]:
        try:
            validate(instance=data, schema=self.schema)
            return True, None
        except jsonschema.exceptions.ValidationError as e:
            return False, e.message


    def _generate_resume_content(self, job_description, background_info) -> Dict:
        chat_handler = ChatHandler()
        intro_session = [
            {
                "role": "system",
                "content": f"Generate a JSON formatted resume based on the following job/PhD description: {job_description}. Use information of a person with this background: {background_info}, as detailed in the schema."

            }
        ]
        response = chat_handler.chat_completion_request(
            intro_session = intro_session,
            functions=[self.setResumeFunctionSpec],
            function_call={"name": "setResume"}
            )

      
        response_data = json.loads(response.function_call.arguments)
        return response_data

    


    def collect_resume_data(self, job_description, background_info, personal_info, save_if_invalid=False):
        resume_content = {}
        resume_content.update(personal_info)
        resume_content.update(self._generate_resume_content(job_description, background_info))
        is_valid, error_message = self._validate_json(resume_content)
        if not is_valid:
            if save_if_invalid:
                with open("invalid_resume.json", "w") as f:
                    json.dump(resume_content, f, indent=4)

            raise Exception(f"Invalid JSON: {error_message}")
   
        return resume_content



    # Create a LaTeX resume
    def create_latex_resume(self, resume_content) -> str:
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self.template_path)
        output = template.render(**resume_content)
        return output

