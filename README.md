# Resume Generator 

This is a simple resume generator that takes background information (in markdown) and a job description (in markdown) and generates a resume (in PDF) that is tailored to the job description.

## Installation

```bash
git clone
cd ResumeGen
poetry install
```

## Usage
Add your background information in `input/background_info.md` and the job description in `input/job_description.md`. You can choose to add a picture of yourself in `input/photo.jpg`. Then run the following command to generate the resume.

```bash
poetry run python main.py
```

Change the resume template by modifying `templates/resume_template.tex.j2`. Change `templates/schema.json` and `templates/FunctionSpec.json` to modify the content sections of the resume generated.




