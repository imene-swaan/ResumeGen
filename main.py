from ResumeGen.resume import ResumeGPT
from ResumeGen.cover import CoverGPT
import frontmatter
import json
from typing import Tuple, Literal



def load_markdown(md_file) -> Tuple[dict, str]:
    with open(md_file, 'r') as file:
        content = file.read()

    # separate the front matter
    content = frontmatter.loads(content)
    return content.metadata, content.content




def main(create: Literal['resume', 'cover'] = 'resume', lang: str = 'english'):
    personal_info, background_info = load_markdown('input/background_info.md')
    _, job_description = load_markdown('input/job_description.md')


    if create == 'cover':
        info = {
            'background_info': background_info,
            'personal_info': personal_info
        }

        generator = CoverGPT()

        cover_content = generator.generate_content(job_description, info, lang)

        # save the motivation content to a file
        with open('cover/cover_letter.txt', 'w') as file:
            file.write(cover_content)

        # read from saved cover letter
        # with open('cover_letter.txt', 'r') as file:
        #     cover_content = file.read()
        
        # generate the cover letter
        cover_latex = generator.generate_latex_cover(cover_content)
        with open('cover/cover_letter.tex', 'w') as file:
            file.write(cover_latex)
        
        compile_latex = input("Do you want to compile the cover letter to PDF? (y/n): ")
        if compile_latex == 'y':
            # compile the latex file to PDF using pdflatex
            import subprocess
            subprocess.run(['pdflatex', 'cover/cover_letter.tex'])
            print("Cover letter generated successfully!")
        
        
    
    elif create == 'resume':
        photo_path = 'input/photo.jpg'

        generator = ResumeGPT(templates='templates')

        resume_content = generator.collect_resume_data(job_description, background_info, lang, personal_info)

        include_photo = input("Do you want to include a photo in the resume? (y/n): ")
        if include_photo == 'y':
            resume_content['photo_path'] = photo_path

        else:
            resume_content['photo_path'] = None


        # save the resume content to a file
        with open('resume/resume_content.json', 'w') as file:
            json.dump(resume_content, file, indent=4)

        # generate the resume
        resume_latex = generator.create_latex_resume(resume_content)
        with open('resume/resume.tex', 'w') as file:
            file.write(resume_latex)

        
        compile_latex = input("Do you want to compile the resume to PDF? (y/n): ")
        if compile_latex == 'y' or compile_latex == '':
            import subprocess
            subprocess.run(['pdflatex', 'resume/resume.tex'])
            print("Resume generated successfully!")

    else:
        print("Invalid type. Please choose 'resume' or 'motivation'.")
    

if __name__ == "__main__":
    lang = "English"

    main("cover", lang)

    # main("resume", lang)

