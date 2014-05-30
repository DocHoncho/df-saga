import re
import png



def load_parameter_map(fn, fn_data):
    map_type, region_name, year, _ = fn_data
    rdr = png.Reader(filename=fn)


map_type_regexps = [
        (re.compile(r'^world_graphic-(\w{3})-(.*)-(\d+)--(\d+).*$'), 'parameter_map', )
        (re.compile(r'^world_graphic-(.*)-(\d+)--(\d+).*$'), 'std_map', )
        (re.compile(r'^world_map-(.*)-(\d+)--(\d+).*$'), 'ascii_map', )
        ]

if __name__ == '__main__':
    :w



