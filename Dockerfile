FROM python:3.10

RUN pip install --upgrade pip

RUN adduser user
USER user
WORKDIR /home/user/zoopla_web_service_full

COPY --chown=user:user requirements.txt requirements.txt
COPY --chown=user:user main.py main.py
RUN pip install --user -r requirements.txt

ENV PATH="/home/user/zoopla_web_service_full/.local/bin:${PATH}"

COPY --chown=user:user . .

CMD python main.py

