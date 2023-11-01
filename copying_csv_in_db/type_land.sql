-- Загрузка данных из type_land.csv в таблицу type_land
COPY type_land(gid, name)
FROM 'D:\backend-electronic-region\type_land.csv' WITH CSV HEADER;