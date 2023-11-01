-- Загрузка данных из land_plot.csv в таблицу land_plot
COPY land_plot(gid, name, area, status, date_create, description, poligon, type_land)
FROM 'D:\backend-electronic-region\land_plot.csv' WITH CSV HEADER ;

-- Обновление поля "area" в таблице "land_plot" с вычисленными площадями в гектарах
UPDATE land_plot
SET area = (ST_Area(poligon::geography) / 10000);

-- Обновление поля "status" в таблице "land_plot" на основе пересечения с дорогами
UPDATE land_plot
SET status = EXISTS (
    SELECT 1
    FROM road
    WHERE ST_Intersects(land_plot.poligon, road.geom)
);