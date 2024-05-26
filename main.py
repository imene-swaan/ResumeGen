from ResumeGen.resume import ResumeGPT
import frontmatter
import json
from typing import Dict, Tuple



def load_markdown(md_file) -> Tuple[dict, dict]:
    with open(md_file, 'r') as file:
        content = file.read()

    # remove the front matter
    content = frontmatter.loads(content)
    return content.metadata, content.content





# Main function
def main():
    personal_info, background_info = load_markdown('input/background_info.md')
    _, job_description = load_markdown('input/job_description.md')

    photo_path = 'input/photo.jpg'

    generator = ResumeGPT(templates='templates')

    resume_content = generator.collect_resume_data(job_description, background_info, personal_info)

    include_photo = input("Do you want to include a photo in the resume? (y/n): ")
    if include_photo == 'y':
        resume_content['photo_path'] = photo_path

    else:
        resume_content['photo_path'] = None


    # save the resume content to a file
    with open('resume_content.json', 'w') as file:
        json.dump(resume_content, file, indent=4)

    # generate the resume
    resume_latex = generator.create_latex_resume(resume_content)
    with open('resume.tex', 'w') as file:
        file.write(resume_latex)

    
    compile_latex = input("Do you want to compile the resume to PDF? (y/n): ")
    if compile_latex == 'y':
        # compile the latex file to PDF using pdflatex
        import subprocess
        subprocess.run(['pdflatex', 'resume.tex'])

        print("Resume generated successfully!")
    

if __name__ == "__main__":
    main()
