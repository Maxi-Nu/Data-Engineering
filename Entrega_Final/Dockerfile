USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
         vim \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
USER airflow

RUN pip install yfinance
RUN pip install psycopg2-binary
RUN pip install sendgrid
RUN pip install SQLAlchemy==1.4.38
RUN pip install pandas
RUN pip install requests