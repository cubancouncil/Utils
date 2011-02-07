import os

"""
Compression configuration example file. Copy this and update the below with your own local settings into settings.py
"""

compress_root = '/path/to/my/site/root/http/_lib/'

compress_files = {
    'js': {
        
        # Outputs /path/to/my/site/root/http/_lib/js/oldspice.min.js, compressing all files in tuple
        
        'js/oldspice.min.js': (
            'js/jquery.js',
            'js/jquery.easing.js',
            'js/oldspice.js'
        ),
        
        # Outputs /path/to/my/site/root/http/_lib/js/product_detail.min.js, compressing the single file given
        
        'js/product_detail.min.js': 'js/product_detail.js'
    },
    'css': {
        # Same idea as JS...
    }
}