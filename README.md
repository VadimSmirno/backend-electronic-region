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
	poligon geometry NOT NULL,
        type_land integer,
	CONSTRAINT land_plot_pkey PRIMARY KEY (gid),
        CONSTRAINT type_land_fk FOREIGN KEY (type_land)
);
```
### Таблица `Тип ЗУ` 
```sql
CREATE TABLE type_land (
	gid integer NOT NULL,
	name character varying, 
	CONSTRAINT type_land_pkey PRIMARY KEY (gid)
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

# Практические задачи




## Задача №1

Написать функцию для загрузки дынных из csv файлов (land_plot.csv, road.csv, type_land.csv) в таблцы (land_plot, road, type_land). 
Дополнительно произвести обработку пространственных данных:
- рассчитать длинну каждой дороги (таблица road, поле geom), результат сохранить в поле len. Единицы измерения километры.
- рассчитать площадь каждого ЗУ (таблица land_plot, поле poligon), результат сохранить в поле area. Единицы измерения гектары.
- проверить пересчение каждого ЗУ с дорогами, результат занести в поле status таблицы land_plot (если ЗУ пересекает хотя бы одну дорогу status = true).

## Задача №2

Написать функцию для отображения информации о маршрутах к центру ЗУ. Для поиска маршрутов использовать API запрос к сервису [OSRM](https://project-osrm.org/docs/v5.24.0/api/#route-service).

На входе функция должна принимать атрибуты: 
- идентификатор ЗУ (land_plot.gid)
- произвольная координата (например 59.216913, 39.866580). 

Вывод функции: 
```
###Самый короткий маршрут
Расстояние - 150км
Время в пути - 10ч 20мин
#Точки маршрута:
1. ключевая точка 1 (3км, 20мин)
2. ключевая точка 2 (23км, 120мин)
...

###Дополнительные машруты (основная информация)
1. Расстояние 200км, 15ч 20мин
2. ...
3. ...
```
Примечание:
- реализовать с помощью команд Django.
- будет плюсом написание тестов

## Задача №3

Необходимо реализовать web-приложение с использованием фреймворка Django и СУБД PostgreSQL для работы с пространственными объектами. 
 
Обеспечить следующие возможности.
1. Авторизация в системе
2. Просмотр списка ЗУ с атрибутивной информацией (номер по порядку, name, area) в табличном виде
3. Просмотр подробной информации о ЗУ на отдельной странице с отображением всех атрибутов

Примечания
- не допускается использование интерфейса администратора Django для реализации страниц
- для верстки использовать bootstrap
- в части frontend допускается использование любых библиотек и плагинов

Будет плюсом
- реализация загрузки данных в таблицу ЗУ посредством API, пагинация
- использование чистых запросов для расчета расстояния

# Работа с базой данных PostgreSQL
## Задача №1

Напишите SQL запрос для поиска ближайшей дороги (road) для каждого ЗУ (land_plot). Результат выполнения запроса должен отображать всю информацию о ЗУ, а также наименование дороги (name) и расстояние до ближайшей точки дороги (если расстояние меньше километра отображать в метрах, елси больше то в километрах).

Дополнительное задание:
 - отображение на странице с подробной информацией о ЗУ из практического задания №3 информации о ближайшей дороге (наименование и расстояние). Расчет должен выполняться "на лету".


# Рефакторинг
Задачи на работу с чужим кодом.
## Задача №1
Посмотрите на код:

```python
class html_copy_to:
    ###  
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
```

Что можно улучшить? Как бы вы его переписали?


## Комментарии

Результат выполнения задания нужно будет оформить здесь же, на гитхабе.
В качестве ответа не нужно присылать никаких(!) ZIP архивов и наборов файлов. Все ваши ответы должны быть оформлены на https://github.com/ .
Вы присылаете только ссылку на ваш репозиторий. У нас в компании применяется GIT, и если вы его не знаете, вам стоит освоить базу самостоятельно.
Если у вас еще нет аккаунта, то это хороший повод его завести.

Если есть вопросы, вы всегда их можете задать, связавшись с человеком, который выдал вам задание.
