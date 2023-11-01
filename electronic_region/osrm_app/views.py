import psycopg2
import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from .forms import LandPlotRouteForm


@login_required
def find_routes_to_land_plot(request, land_plot_gid, start_point_lat, start_point_lon):
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password= settings.DATABASES['default']['PASSWORD'],
        host= settings.DATABASES['default']['HOST']
    )

    cur = conn.cursor()
    try:
        # Получение координат центра ЗУ (land_plot.gid) из базы данных
        cur.execute("SELECT ST_X(ST_Centroid(poligon)), ST_Y(ST_Centroid(poligon)) FROM land_plot WHERE gid = %s;",
                    (land_plot_gid,))
        land_plot_coordinates = cur.fetchone()

        if land_plot_coordinates:
            osrm_url = 'https://router.project-osrm.org/route/v1/driving/'
            url = f'{osrm_url}{land_plot_coordinates[1]},{land_plot_coordinates[0]};{start_point_lat},{start_point_lon}?alternatives=true'

            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                distance = data['routes'][0]['distance'] / 1000  # Расстояние в километрах
                duration = data['routes'][0]['duration'] / 3600  # Время в часах
                waypoints = data['waypoints']

                context = {
                    'distance': distance,
                    'duration': duration,
                    'waypoints': waypoints
                }

                return render(request, 'info_routes_template.html', context=context)
            else:
                return HttpResponse("Ошибка при выполнении запроса к сервису OSRM")
        else:
            return HttpResponse("ЗУ с указанным gid не найдено в базе данных")
    finally:
        cur.close()
        conn.close()


@login_required
def find_route(request):
    if request.method == 'POST':
        form = LandPlotRouteForm(request.POST)
        if form.is_valid():
            land_plot_gid = form.cleaned_data['land_plot_gid']
            start_point_lat = form.cleaned_data['start_point_lat']
            start_point_lon = form.cleaned_data['start_point_lon']

            url = reverse('find_routes', args=[land_plot_gid, start_point_lat, start_point_lon])
            return redirect(url)
    else:
        form = LandPlotRouteForm()
    return render(request, 'form_template.html', {'form': form})


@login_required
def land_plot_list(request):
    # Подключение к базе данных
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST']
    )

    cur = conn.cursor()
    with cur as cursor:
        cursor.execute("SELECT gid, name, area FROM land_plot ORDER BY gid")
        land_plots = cursor.fetchall()
    paginator = Paginator(land_plots, 10)  # 10 элементов на странице
    page = request.GET.get('page')  # Получите номер страницы из параметра запроса
    land_plots = paginator.get_page(page)

    context = {
        'land_plots': land_plots
    }
    return render(request, 'land_plot_list.html', context)


@login_required
def land_plot_detail(request, land_plot_id):
    conn = psycopg2.connect(
        dbname=settings.DATABASES['default']['NAME'],
        user=settings.DATABASES['default']['USER'],
        password=settings.DATABASES['default']['PASSWORD'],
        host=settings.DATABASES['default']['HOST']
    )

    cur = conn.cursor()
    with cur as cursor:
        cursor.execute("""
            SELECT
                lp.gid, lp.name AS land_plot_name, lp.area, lp.status, lp.date_create,
                lp.description, lp.poligon, lp.type_land,
                r.name AS road_name,
                CASE
                    WHEN ST_Distance(lp.poligon::geography, r.geom::geography) < 1000 THEN
                        ROUND(ST_Distance(lp.poligon::geography, r.geom::geography)::numeric,2) || ' м'
                    ELSE
                        ROUND(ST_Distance(lp.poligon::geography, r.geom::geography)::numeric / 1000 ,2 )  || ' км'
                END AS distance_to_nearest_road
            FROM
                land_plot lp
            LEFT JOIN
                road r
            ON
                ST_DWithin(lp.poligon, r.geom, 0.1)
            WHERE
                lp.gid = %s
        """, [land_plot_id])
        land_plot = cursor.fetchone()

    context = {
        'land_plot': land_plot
    }
    return render(request, 'land_plot_detail.html', context)


class HomeView(TemplateView):
    template_name = 'home.html'
