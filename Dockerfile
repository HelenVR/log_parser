FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ARG APP_DIR=/usr/log_parser
ENV PATH $APP_DIR:$PATH
WORKDIR $APP_DIR
COPY . ./

ENV VIRTUAL_ENV "${APP_DIR}/venv"
RUN python3.12 -m venv $VIRTUAL_ENV
ENV PATH "$VIRTUAL_ENV/bin:$PATH"

RUN pip3.12 install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-root --only main

ENV APP_PORT=8040
ENV APP_HOST=127.0.0.1
EXPOSE ${APP_PORT}
CMD ["sh", "-c", "uvicorn log_parser.main:app --host $APP_HOST --port $APP_PORT"]
