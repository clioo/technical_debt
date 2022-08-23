FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN apt-get update

RUN apt install -y g++ curl
RUN apt-get install -y unixodbc-dev
RUN apt-get install -y libgl1-mesa-glx libglib2.0-0
RUN apt-get install -y wget ca-certificates gnupg2
RUN apt-get install -y gcc libc-dev musl-dev build-essential

# Add SQL Server ODBC Driver 17 for Ubuntu 18.04
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
 && curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list \
 && apt-get update -y --allow-releaseinfo-change \
 && ACCEPT_EULA=Y apt-get install -y msodbcsql17 \
 && apt-get -y clean

### Copy app directory and install local packages ###
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY ./app /app
