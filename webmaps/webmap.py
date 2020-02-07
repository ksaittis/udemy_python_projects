from folium import Map, Marker, Icon, FeatureGroup, Popup, CircleMarker, GeoJson, LayerControl
import webbrowser
import os
import random
import pandas

MAP_FILENAME: str = "map.html"


def generate_web_map_html(filename: str) -> None:
    map = Map(location=[48.7767982, -121.8109970])
    volcanoes_feature_group = get_volcanoes_feature_group()
    population_feature_group = get_population_feature_group()
    map.add_child(volcanoes_feature_group)
    map.add_child(population_feature_group)
    map.add_child(LayerControl())
    map.save(filename)


def add_random_markers(feature_group: FeatureGroup) -> FeatureGroup:
    for i in range(random.randint(5, 10)):
        feature_group.add_child(
            child=Marker(location=[51.7522202 + random.uniform(-0.1, 0.1), -1.25596 + random.uniform(-0.1, 0.1)],
                         popup="Marker", icon=Icon()))
    return feature_group


def get_elevation_color(elevation: float) -> str:
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


def get_volcanoes_feature_group() -> FeatureGroup:
    feature_group = FeatureGroup(name="Volcanoes")
    data = pandas.read_csv("./Volcanoes_USA.txt")
    latitudes = list(data['LAT'])
    longitudes = list(data['LON'])
    elevation = list(data['ELEV'])
    for lat, lon, elev in zip(latitudes, longitudes, elevation):
        feature_group.add_child(
            CircleMarker(location=(lat, lon), color='grey', weight=1, radius=6,
                         popup=Popup(str(elev) + "m", parse_html=True),
                         fill_color=get_elevation_color(elev)))
    return feature_group


def get_population_feature_group() -> FeatureGroup:
    population_feature_group = FeatureGroup('Population')
    population_feature_group.add_child(GeoJson(data=open('world.json', mode='r', encoding='utf-8-sig').read(),
                                               style_function=lambda x: {
                                                   'fillColor': 'green' if x['properties']['POP2005'] < 10000000
                                                   else 'orange' if 10000000 <= x['properties'][
                                                       'POP2005'] < 20000000 else 'red'}))
    return population_feature_group


def open_webmap(filename: str) -> None:
    webbrowser.open('file://' + os.path.realpath(filename))


if __name__ == "__main__":
    generate_web_map_html(MAP_FILENAME)
    open_webmap(MAP_FILENAME)
