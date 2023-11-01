-- Загрузка данных из road.csv в таблицу road
COPY road(gid, name, status, geom, len)
FROM 'D:\backend-electronic-region\road.csv' WITH CSV HEADER NULL 'NULL';

-- Обновление поля "len" в таблице "road" с вычисленными длинами в километрах
UPDATE road
SET len = ST_Length(geom::geography) / 1000;