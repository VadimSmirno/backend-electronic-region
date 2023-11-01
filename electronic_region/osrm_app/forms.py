from django import forms

class LandPlotRouteForm(forms.Form):
    land_plot_gid = forms.IntegerField(label="Идентификатор ЗУ")
    start_point_lat = forms.FloatField(
        label="Широта (пример: 59,216913)",
        widget=forms.NumberInput(),
        initial=59.216913
    )
    start_point_lon = forms.FloatField(
        label="Долгота (пример: 39,866580)",
        widget=forms.NumberInput(),
        initial=39.866580
    )