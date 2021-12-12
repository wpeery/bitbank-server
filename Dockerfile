FROM python:3.8.12
# not sure what these two lines do but they were in
# an example I found.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update \
    && apt-get install -y ipython3 vim git
WORKDIR /bitbank/workspace
COPY requirements/ /bitbank/requirements/
RUN python -m pip install --upgrade pip
RUN pip install -r /bitbank/requirements/local.txt
