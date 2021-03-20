FROM infrastructureascode/uwsgi

WORKDIR /usr/src/app

ENV UWSGI_INI /usr/src/app/uwsgi.ini

EXPOSE 5000

COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt


COPY . .

CMD ["uwsgi", "/usr/src/app/uwsgi.ini", "-b", "32768"]