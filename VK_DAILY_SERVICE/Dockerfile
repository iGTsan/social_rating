FROM python:3.11-slim

WORKDIR "/social_rating_Kraft_Bot"

COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD python3 daily_service.py ${LOCAL} ${PRODIGY} ${DEBUG}
