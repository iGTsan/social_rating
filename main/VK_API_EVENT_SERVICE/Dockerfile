FROM python:3.11-slim

WORKDIR "/Dick_Kraft_Bot"

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 vk_api_event_service.py ${LOCAL} ${PRODIGY} ${DEBUG}
