# Тестовое задание на позицию backend-разработчик

## Задача №1

Необходимо реализовать web-приложение с использованием фреймворка Django и СУБД PostgreSQL для работы с пространственными объектами. 

Обозначения 
ЗУ - земельный участок

Обеспечить следующие возможности.
1. Авторизация в системе
2. Просмотр списка ЗУ с атрибутивной информацией (номер по порядку, name, area) в табличном виде
3. Просмотр подробной информации о ЗУ на отдельной странице с отображением дополнительных атрибутов (status, date_status, description)
4. Отображение на странице с подробной информацией наименования ближайшей дороги и расстояния до неё

Примечания
- не допускается использование интерфейса администратора Django для реализации страниц 
- в части frontend допускается использование любых библиотек и плагинов

Будет плюсом
- реализация загрузки данных в таблицу ЗУ посредством API, пагинация
- использование чистых запросов для расчета расстояния

### Таблица `Земельные участки`

```sql
CREATE TABLE land_plot (
	gid integer NOT NULL,
	name character varying NOT NULL,
	area float NOT NULL,
	status boolean,
	date_status timestamp with time zone, 
	description text,
	poligon geometry NOT NULL
	CONSTRAINT land_plot_pkey PRIMARY KEY (gid)
);
```
### Таблица `Дороги`
```
CREATE TABLE IF NOT EXISTS road
(
    gid integer,
    name character varying,
    status boolean, 
    geom geometry NOT NULL,
    CONSTRAINT road_transport_pk PRIMARY KEY (gid),
     
)
```
