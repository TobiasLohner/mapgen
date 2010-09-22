import os.path
import subprocess
from georect import GeoRect

cmd_ogr2ogr = "ogr2ogr"

__maps = ["eur", "noa", "sas", "soa"]
__layers = [["pop-miscellaneous-population-p", "mispopppop_point", "", "txt"],
            ["pop-built-up-a", "builtupapop_area", "", "nam"],
            ["hydro-water-course-l", "watrcrslhydro_line", "hyc=8", "nam"],
            ["hydro-inland-water-a", "inwaterahydro_area", "hyc=8", "nam"],
            ["trans-railroad-l", "railrdltrans_line", "exs=28", "fco"],
            ["trans-road-l", "roadltrans_line", "rtt=14", "med"]]
        
def copy_clipped(rc, dir_data, dir_temp):
    files = []
    for layer in __layers:
        print "Creating topology layer " + layer[1] + " ..."

        for i in range(len(__maps)):
            arg = [cmd_ogr2ogr]
            
            if i > 0:
                arg.append("-update")
                arg.append("-append")
            else:
                arg.append("-overwrite")
                
            if layer[1] != "":
                arg.append("-where")
                arg.append(layer[2])
                
            arg.append("-select")
            arg.append(layer[3])
            
            arg.append("-spat")
            arg.append(str(rc.left.value_degrees())) 
            arg.append(str(rc.bottom.value_degrees())) 
            arg.append(str(rc.right.value_degrees()))
            arg.append(str(rc.top.value_degrees()))

            arg.append(dir_temp)
            arg.append(os.path.join(dir_data, __maps[i]))

            arg.append(layer[0])
            arg.append("-nln")
            arg.append(layer[1])
            
            p = subprocess.Popen(arg)
            p.wait()
            
        if os.path.exists(os.path.join(dir_temp, layer[1] + ".shp")):
            files.append([os.path.join(dir_temp, layer[1] + ".shp"), True])   
            files.append([os.path.join(dir_temp, layer[1] + ".shx"), True])   
            files.append([os.path.join(dir_temp, layer[1] + ".dbf"), True])   
            files.append([os.path.join(dir_temp, layer[1] + ".prj"), True])   
        
    return files
        
            
def generate_tpl_file(dir_temp):
    file = open(os.path.join(dir_temp, "topology.tpl"), "w")
    file.write("* filename,range,icon,field\n");
    file.write("inwaterahydro_area, 100,,,64,96,240\n");
    file.write("watrcrslhydro_line,    7,,,64,96,240\n");
    file.write("builtupapop_area,  15,,1,223,223,0\n");
    file.write("roadltrans_line,     15,,,240,64,64\n");
    file.write("railrdltrans_line,   10,,,64,64,64\n");
    file.write("mispopppop_point,    5,218,1,223,223,0\n");
    file.close()
    return os.path.join(dir_temp, "/topology.tpl")

def Create(bounds, dir_data = "../data/", dir_temp = "../tmp/"):
    dir_data = os.path.abspath(os.path.join(dir_data, "vmap0")) 
    dir_temp = os.path.abspath(dir_temp) 
    
    files = copy_clipped(bounds, dir_data, dir_temp)
    files.append([generate_tpl_file(dir_temp), True])
        
    return files