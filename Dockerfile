FROM python:3.8.0
COPY . /
RUN pip install -r requirements.txt
EXPOSE 5000
COPY ./docker_entrypoint.sh /
RUN chmod +x /docker_entrypoint.sh
ENTRYPOINT ["/docker_entrypoint.sh"]