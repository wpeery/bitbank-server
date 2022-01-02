FROM python:3.9.9
# Do not generate pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Output is sent straight to terminal without being first buffered
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get install -y ipython3 vim git postgresql-client-13 redis-tools
COPY requirements/ /bitbank/requirements/
RUN python -m pip install --upgrade pip
RUN pip install -r /bitbank/requirements/local.txt
RUN useradd -r -u 1000 dev-env-user
USER dev-env-user
WORKDIR /bitbank/workspace
