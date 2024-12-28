FROM python:3.13.1-bullseye

RUN pip install poetry

COPY . .

RUN poetry install

ENTRYPOINT ["poetry", "run", "python", "-m", "testing_project.main"]