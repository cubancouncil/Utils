import os
from fabric.api import *

"""
Cuban Council fabfile. Some might say the fabbest of all.

"""

# ---- Variables

# Compression path root. Used as relative path for all paths set in 'compress_files' var

compress_root = os.path.dirname(os.path.dirname(__file__)) 

# File list by type, to be compressed. Dictionary entries in css/js -- key is outgoing file path relative to 'compress_root', and 
# value is either a string file path relative to 'compress_root' or a tuple of string file paths to minify together into the outgoing 
# file. See settings_example.py for example

compress_files = {
    'css': {},
    'js': {}
}

# Import local settings, if available

try:
    from settings import *
except ImportError:
    pass

# ---- Functions

def compress():
    
    """
    Compress/minify CSS and JS resources according to paths configured with 'compress_files' variable
    
    """
    
    # Get resource root path

    for file_type in compress_files:
        for out_file in compress_files[file_type]:

            # Set out directory and file

            out_file_path = os.path.join(compress_root, out_file).replace('\\', '/')

            # Get list of files to compress

            if type(compress_files[file_type][out_file]) is str:
                file_list = tuple([compress_files[file_type][out_file]])
            else:
                file_list = compress_files[file_type][out_file]

            # Cycle through and compress files

            file_list = ' '.join('\'' + os.path.join(compress_root, in_file).replace('\\', '/') + '\'' for in_file in file_list)
            cmd = 'awk 1 %s | java -jar yuicompressor-2.4.2.jar --type %s -o %s' % (file_list, file_type, out_file_path)
            local(cmd, capture=False)