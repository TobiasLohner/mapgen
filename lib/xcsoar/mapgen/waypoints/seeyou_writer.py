from xcsoar.mapgen.waypoints.list import WaypointList

def __compose_line(waypoint):
    # "Aachen Merzbruc",AACHE,DE,5049.383N,00611.183E,189.0m,5,80,530.0m,"122.875",
    str = '"' + waypoint.name + '",'
    str += waypoint.short_name + ','
    str += waypoint.country_code + ','
    
    lat = abs(waypoint.lat)
    str += "{:02d}".format(int(lat))
    lat = round((lat - int(lat)) * 60, 3)
    str += "{:06.3f}".format(lat)
    if waypoint.lat > 0: str += 'N,' 
    else: str += 'S,'
    
    lon = abs(waypoint.lon)
    str += "{:03d}".format(int(lon))
    lon = round((lon - int(lon)) * 60, 3)
    str += "{:06.3f}".format(lon)
    if waypoint.lon > 0: str += 'E,' 
    else: str += 'W,'
    
    elev = abs(waypoint.altitude)
    str += "{:.1f}m,".format(elev)
    
    if waypoint.type:
        if waypoint.type == 'outlanding': str += "3,"
        elif waypoint.type == 'glider_site': str += "4,"
        elif waypoint.type == 'airport': 
            if (waypoint.surface and (waypoint.surface == 'concrete' or 
                                      waypoint.surface == 'asphalt')): 
                str += "5,"
            else: 
                str += "2,"
        elif waypoint.type == 'mountain pass': str += "6,"
        elif waypoint.type == 'mountain top': str += "7,"
        elif waypoint.type == 'tower': str += "8,"
        elif waypoint.type == 'tunnel': str += "13,"
        elif waypoint.type == 'bridge': str += "14,"
        elif waypoint.type == 'powerplant': str += "15,"
        elif waypoint.type == 'castle': str += "16,"
        elif waypoint.type.endswith('junction'): str += "17,"
        elif waypoint.type.endswith('cross'): str += "17,"
        else: str += "1,"
    else: str += "1,"

    if waypoint.runway_dir:
        str += "{:03d}".format(waypoint.runway_dir)
        
    str += ','
    if waypoint.runway_len:
        str += "{:03d}.0m".format(waypoint.runway_len)
        
    str += ','
    if waypoint.freq:
        str += "{:07.3f}".format(waypoint.freq)
        
    str += ','
    return str

def write_seeyou_waypoints(waypoints, path):
    if not isinstance(waypoints, WaypointList): 
        raise TypeError("WaypointList expected")
    
    with open(path, "w") as f:
        for waypoint in waypoints:
            f.write(__compose_line(waypoint) + '\r\n')
    
    return path
