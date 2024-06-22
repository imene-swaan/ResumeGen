from ResumeGen.LLMs.gpt import ChatHandler
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from typing import Union


class CoverGPT:
    def __init__(
            self,
            templates: Union[Path, str] = "templates",
            ):
        self.template_path = f"{templates}/cover_template.tex.j2"
        with open(self.template_path, "r") as f:
            self.template = f.read()

        

    def generate_content(self, job_description, background_info, lang='en'):
        chat_handler = ChatHandler()
        intro_session = [
            {
                "role": "system",
                "content": f"Generate a cover letter for me in {lang} based on the following job description: {job_description}. Use my personal information and background: {background_info}. Mention why I am interested in the position, how I can contribute to the company, and where I see myself in the future. Make the necessary adjustments to create a letter according to this LaTeX template: {self.template}"
            }
        ]
        response = chat_handler.chat_completion_request(
            intro_session = intro_session
            )
        return response
    
    def Spacyfy(self, text:str):
        return text.replace('\n', '\n\n')


    def generate_latex_cover(self, cover_content):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self.template_path)
        output = template.render(cover_text=self.Spacyfy(cover_content))
        return output


        

    




    





