from folium import Map, Marker, Icon, FeatureGroup, Popup
import webbrowser, os
import random
import pandas

MAP_FILENAME: str = "map.html"


def generate_web_map_html(filename: str) -> None:
    map = Map(location=[51.7522202, -1.25596])
    feature_group = FeatureGroup(name="My map")
    updated_feature_group = add_markers_for_volcanoes(feature_group)
    map.add_child(updated_feature_group)
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


def add_markers_for_volcanoes(feature_group: FeatureGroup) -> FeatureGroup:
    data = pandas.read_csv("Volcanoes_USA.txt")
    latitudes = list(data['LAT'])
    longitudes = list(data['LON'])
    elevation = list(data['ELEV'])
    for lat, lon, elev in zip(latitudes, longitudes, elevation):
        feature_group.add_child(Marker(location=[lat, lon], popup=Popup(str(elev) + "m", parse_html=True),
                                       icon=Icon(get_elevation_color(elev))))
    return feature_group


def open_webmap(filename: str) -> None:
    webbrowser.open('file://' + os.path.realpath(filename))


if __name__ == "__main__":
    generate_web_map_html(MAP_FILENAME)
    open_webmap(MAP_FILENAME)
    # os.remove(MAP_FILENAME)
