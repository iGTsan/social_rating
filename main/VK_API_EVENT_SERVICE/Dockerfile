FROM python:3.11-slim

WORKDIR "/Dick_Kraft_Bot"

COPY . ./

COPY ../INIT_DATA ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 DKB.py ${LOCAL} ${PRODIGY} ${DEBUG}
