import os
from fabric.api import *

"""
Cuban Council fabfile. Some might say the fabbest of all.

"""

# ---- Variables

# Compression path root. Used as relative path for all paths set in 'env.compress_files' var

env.compress_root = os.path.dirname(os.path.dirname(__file__)) 

# File list by type, to be compressed. Dictionary entries in css/js -- key is outgoing file path relative to 'env.compress_root', and 
# value is either a string file path relative to 'env.compress_root' or a tuple of string file paths to minify together into the outgoing 
# file. See settings_example.py for example

env.compress_files = {
    'css': {},
    'js': {}
}

# Import local settings, if available

try:
    from settings import *
except ImportError:
    pass

# ---- Functions

def pushkey(keytype='dsa'):
    
    """
    Put your local SSH key on an indicated remote host
    
    Usage:
    
        fab pushkey
    
    If not using DSA, pass in key type to use:
    
        fab pushkey:rsa
    
    To push to a specific host:
    
        fab -H someserver.com pushkey
    
    """
    
    publickey = '~/.ssh/id_%s.pub' % keytype
    tmpfile = '/tmp/%s.pub' % env.user
    
    run('mkdir -p ~/.ssh && chmod 700 ~/.ssh')
    put(publickey, tmpfile)
    run('cat %s >> ~/.ssh/authorized_keys' % tmpfile)
    run('rm %s' % tmpfile)

def compress():
    
    """
    Compress/minify CSS and JS resources according to paths configured with 'env.compress_files' variable
    
    """
    
    # Get resource root path

    for file_type in env.compress_files:
        for out_file in env.compress_files[file_type]:

            # Set out directory and file

            out_file_path = os.path.join(env.compress_root, out_file).replace('\\', '/')

            # Get list of files to compress

            if type(env.compress_files[file_type][out_file]) is str:
                file_list = tuple([env.compress_files[file_type][out_file]])
            else:
                file_list = env.compress_files[file_type][out_file]

            # Cycle through and compress files

            file_list = ' '.join('\'' + os.path.join(env.compress_root, in_file).replace('\\', '/') + '\'' for in_file in file_list)
            cmd = 'awk 1 %s | java -jar yuicompressor-2.4.6.jar --type %s -o %s' % (file_list, file_type, out_file_path)
            local(cmd, capture=False)