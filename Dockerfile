FROM python:latest

RUN pip install -U Flask
RUN mkdir /python_wiki/
COPY ./ /python_wiki/

WORKDIR /python_wiki/

CMD [ "python", "main.py" ]