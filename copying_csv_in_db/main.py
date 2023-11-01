import psycopg2
from decouple import config

conn = psycopg2.connect(
    dbname=config('POSTGRES_DB'),
    user=config('POSTGRES_USER'),
    password=config('POSTGRES_PASSWORD'),
    host=config("HOST")
)

cur = conn.cursor()

create_land_plot_table = """
CREATE TABLE IF NOT EXISTS land_plot (
    gid serial PRIMARY KEY,
    name character varying,
    area double precision,
    status boolean,
    date_create timestamp with time zone,
    description text,
    poligon geometry NOT NULL,
    type_land integer,
    CONSTRAINT type_land_fk FOREIGN KEY (type_land) REFERENCES type_land(gid)
);
"""

create_type_land_table = """
CREATE TABLE IF NOT EXISTS type_land (
    gid serial PRIMARY KEY,
    name character varying
);
"""

create_road_table = """
CREATE TABLE IF NOT EXISTS road (
    gid serial PRIMARY KEY,
    name character varying,
    len double precision,
    status boolean,
    geom geometry NOT NULL
);
"""
# Загрузка данных из CSV файла в таблицу road
copy_query = """
COPY road(gid, name, status, geom, len)
FROM 'D:/backend-electronic-region/road.csv' WITH CSV HEADER NULL 'NULL';
"""
# Загрузка данных из CSV файла в таблицу land_plot
copy_query_land_plot = """
COPY land_plot(gid, name, area, status, date_create, description, poligon, type_land)
FROM 'D:/backend-electronic-region/land_plot.csv' WITH CSV HEADER;
"""

# Загрузка данных из CSV файла в таблицу type_land
copy_query_type_land = """
COPY type_land(gid, name)
FROM 'D:/backend-electronic-region/type_land.csv' WITH CSV HEADER;
"""

# Обновление поля "len" в таблице "road" с вычисленными длинами в километрах
update_query = """
UPDATE road
SET len = ST_Length(geom::geography) / 1000;
"""
# Обновление поля "area" в таблице "land_plot" с вычисленными площадями в гектарах
update_area_query = """
UPDATE land_plot
SET area = (ST_Area(poligon::geography) / 10000);
"""

# Обновление поля "status" в таблице "land_plot" на основе пересечения с дорогами
update_status_query = """
UPDATE land_plot
SET status = EXISTS (
    SELECT 1
    FROM road
    WHERE ST_Intersects(land_plot.poligon, road.geom)
);
"""

cur.execute(create_land_plot_table)
cur.execute(create_type_land_table)
cur.execute(create_road_table)
cur.execute(copy_query_land_plot)
cur.execute(copy_query_type_land)
cur.execute(copy_query)
cur.execute(update_query)
cur.execute(update_area_query)
cur.execute(update_status_query)

conn.commit()
cur.close()
conn.close()
