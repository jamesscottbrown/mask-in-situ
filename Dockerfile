FROM python:3.8-slim
RUN python -m pip install --upgrade build

RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user

COPY . .
RUN python -m pip install .

USER app_user
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["/bin/bash", "-c"]
