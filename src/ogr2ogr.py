import os.path
import subprocess
from georect import GeoRect

class ogr2ogr:
    __maps = ["eur", "noa", "sas", "soa"]
    __source = "../data/vmap0/"
    __layers = [["pop-miscellaneous-population-p", "mispopppop_point", "", "txt"],
                ["pop-built-up-a", "builtupapop_area", "", "nam"],
                ["hydro-water-course-l", "watrcrslhydro_line", "hyc=8", "nam"],
                ["hydro-inland-water-a", "inwaterahydro_area", "hyc=8", "nam"],
                ["trans-railroad-l", "railrdltrans_line", "exs=28", "fco"],
                ["trans-road-l", "roadltrans_line", "rtt=14", "med"]]
    
    def __init__(self, executable = "ogr2ogr"):
        self.set_executable(executable)
        
    def set_executable(self, executable = "ogr2ogr"):
        self.__executable = os.path.abspath(executable)
        
    def copy_clipped(self, rc, destination):
        for i in range(len(self.__maps)):
            for layer in self.__layers:
                arg = [self.__executable]
                
                if i > 0:
                    arg.append("-update")
                    arg.append("-append")
                    
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

                arg.append(os.path.abspath(destination))
                arg.append(os.path.abspath(self.__source + 
                                           self.__maps[i]))

                arg.append(layer[0])
                arg.append("-nln")
                arg.append(layer[1])
                
                p = subprocess.Popen(arg)
                p.wait()
                
    def generate_tpl_file(self, destination):
        file = open(os.path.abspath(destination) + "/topology.tpl" , "w")
        file.write("* filename,range,icon,field\n");
        file.write("inwaterahydro_area, 100,,,64,96,240\n");
        file.write("watrcrslhydro_line,    7,,,64,96,240\n");
        file.write("builtupapop_area,  15,,1,223,223,0\n");
        file.write("roadltrans_line,     15,,,240,64,64\n");
        file.write("railrdltrans_line,   10,,,64,64,64\n");
        file.write("mispopppop_point,    5,218,1,223,223,0\n");
        file.close()