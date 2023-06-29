FROM --platform=linux/amd64 python:3.9 as python-base

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN python -m pip install --upgrade urllib3==1.26.15
RUN python -m pip install poetry==1.4.2
RUN poetry config virtualenvs.create false

# Отдельный freezer для того, чтобы не пересобирать все приложение при изменении
# версии в pyproject.toml
FROM python-base as freezer

COPY pyproject.toml poetry.lock ./
RUN poetry export -f requirements.txt --output ./requirements.txt --without-hashes

###
FROM python-base as full-image

COPY --from=freezer /app/requirements.txt ./requirements.txt
RUN python -m pip install -r requirements.txt

COPY ls_cleaner ./ls_cleaner

# datapipe --pipeline brickit_pipeline.ls_cleaner:ls_cleaner api
CMD ["python3", "ls_cleaner/clean.py"]
