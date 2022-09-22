FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip cache remove * && pip install --no-cache-dir -r requirements.txt
COPY . /code/
RUN chgrp -R 0 /code && chmod -R g=u /code
ENTRYPOINT ["/code/docker-entrypoint.sh"]
