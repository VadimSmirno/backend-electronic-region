# Тестовое задание на позицию backend-разработчик

### Обозначения 
ЗУ - земельный участок

### Таблица `Земельные участки` 
```sql
CREATE TABLE land_plot (
	gid integer NOT NULL,
	name character varying,
	area double precision,
	status boolean,
	date_create timestamp with time zone, 
	description text,
	poligon geometry NOT NULL
	CONSTRAINT land_plot_pkey PRIMARY KEY (gid)
);
```
### Таблица `Дороги`
```sql
CREATE TABLE road
(
    gid integer,
    name character varying,
    len double precision,
    status boolean, 
    geom geometry NOT NULL,
    CONSTRAINT road_transport_pk PRIMARY KEY (gid) 
)
```

## Задача №1

Написать функцию для загрузки дынных из csv файлов (land_plot.csv, road.csv) в таблцы (land_plot, road). 
Дополнительно произвести обработку пространственных данных:
- рассчитать длинну каждой дороги (таблица road, поле geom), результат сохранить в поле len. Единицы измерения километры.
- рассчитать площадь каждого ЗУ (таблица land_plot, поле poligon), результат сохранить в поле area. Единицы измерения гектары.
- проверить пересчение каждого ЗУ с дорогами, результат занести в поле status таблицы land_plot (если ЗУ пересекает хотя бы одну дорогу status = true).

Реализация на ваше усмотрение, возможно использование ORM Django или чистых запросов SQL.

## Задача №2

Необходимо реализовать web-приложение с использованием фреймворка Django и СУБД PostgreSQL для работы с пространственными объектами. 
 
Обеспечить следующие возможности.
1. Авторизация в системе
2. Просмотр списка ЗУ с атрибутивной информацией (номер по порядку, name, area) в табличном виде
3. Просмотр подробной информации о ЗУ на отдельной странице с отображением всех атрибутов
4. Отображение на странице с подробной информацией наименования ближайшей дороги и расстояния до неё (если расстояние меньше километра отображать в метрах, елси больше то в километрах)

Примечания
- не допускается использование интерфейса администратора Django для реализации страниц
- для верстки использовать bootstrap
- в части frontend допускается использование любых библиотек и плагинов

Будет плюсом
- реализация загрузки данных в таблицу ЗУ посредством API, пагинация
- использование чистых запросов для расчета расстояния

## Задача №3

```python
class html2canvasproxy:
    ###
    def __init__(self, callback, url):
        if callback is not None and re.match('[^A-Za-z0-9_[.]\\[\\]]', callback) is not None:
            self.set_response('error:Parameter "callback" contains invalid characters (' + callback + ')')
        elif url == '' or url is None:
            self.set_response('error:No such parameter "url"')
        elif html2canvasproxy.is_http_url(url) == False:
            self.set_response('error:Only http scheme and https scheme are allowed (' + url + ')')
        else:
            self.callback = callback

            o = urlparse.urlparse(url)

            if o.username is not None:
                self.http_username = o.username

            if o.password is not None:
                self.http_password = o.password

            if self.http_username != '' or self.http_password != '':
                uri = (o.netloc.split('@'))[1]
            else:
                uri = o.netloc

            self.url = o.scheme + '://' + uri + o.path

            if o.query != '':
                self.url += '?' + o.query

    def enable_crossdomain(self):
        self.cross_domain = True;

    def initiate(self):
        if self.status != 0:
            return None

        self.download_source()

    def download_source(self):
        headers = { 'User-Agent' : self.ua }

        if self.ref != '':
            o = urlparse.urlparse(self.ref)
            self.scheme = o.scheme
            self.host = o.netloc

            headers['Referer'] = self.ref

        if self.http_username != '' or self.http_password != '':
            auth = self.http_username + ':' + self.http_password
            auth = auth.encode('ascii')
            auth = base64.b64encode(auth)

            headers['Authorization'] = 'Basic ' + auth

        try:
            req = urllib2.Request(self.url, None, headers)
            r = urllib2.urlopen(req)
            h = r.info()

            if h['Content-Type'] != '' and h['Content-Type'] != None:
                if re.match('^(image|text|application)\/', h['Content-Type']) is None:
                    self.set_response('error:Invalid mime-type: ' + h['Content-Type'])
                else:
                    mime = str(re.sub('[;]([\s\S]+)$', '', h['Content-Type'])).strip().lower()
                    mime = re.sub('/x-', '/', mime)

                    if mime in self.mimes:
                        self.data = r.read()

                        extension = re.sub('^(image|text|application)\/', '', mime)
                        extension = re.sub('(windows[-]bmp|ms[-]bmp)', 'bmp', extension)
                        extension = re.sub('(svg[+]xml|svg[-]xml)', 'svg', extension)
                        extension = extension.replace('xhtml[+]xml', 'xhtml')
                        extension = extension.replace('jpeg', 'jpg')

                        self.real_extension = extension
                        self.real_mimetype  = mime

                        cp = h['Content-Type'].find(';');

                        if cp != -1:
                            cp = cp + 1
                            charset = h['Content-Type']
                            self.real_charset = ';' + charset[cp:].strip()

                        self.save_file()
                    else:
                        self.set_response('error:Invalid mime-type: ' + h['Content-Type'])
            else:
                self.set_response('error:No mime-type defined')

            r.close()
        except urllib2.URLError, e:
            self.set_response('error:SOCKET: ' + str(e.reason))

    def remove_old_files(self):
        a = []
        for f in os.listdir(self.save_path):
            if f.find(self.prefix) == 0 and os.path.isfile(self.save_path + f) and ((self.init_exec - os.path.getctime(self.save_path + f))) > (self.ccache * 2):
                os.unlink(self.save_path + f)

    def save_file(self):
        file_name = hashlib.sha1(self.url).hexdigest()
        tmp_ext = str(random.randrange(1000)) + '_' + str(self.init_exec)

        if os.path.isfile(self.save_path + file_name + '.' + tmp_ext):
            self.save_file() #try again
        else:
            f = open(self.save_path + file_name + '.' + tmp_ext, 'wb')
            f.write(self.data)
            f.close()

            if os.path.isfile(self.save_path + file_name + '.' + self.real_extension):
                os.remove(self.save_path + file_name + '.' + self.real_extension)

            os.rename(self.save_path + file_name + '.' + tmp_ext, self.save_path + file_name + '.' + self.real_extension)

            self.set_response(self.scheme + '://' + self.host + self.route_path + file_name + '.' + self.real_extension)
```



## Комментарии

Результат выполнения задания нужно будет оформить здесь же, на гитхабе.
В качестве ответа не нужно присылать никаких(!) ZIP архивов и наборов файлов. Все ваши ответы должны быть оформлены на https://github.com/ .
Вы присылаете только ссылку на ваш репозиторий. У нас в компании применяется GIT, и если вы его не знаете, вам стоит освоить базу самостоятельно.
Если у вас еще нет аккаунта, то это хороший повод его завести.

Если есть вопросы, вы всегда их можете задать, связавшись с человеком, который выдал вам задание.
