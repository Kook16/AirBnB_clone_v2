#!/usr/bin/python3
'''A Fabric script that generates a .tar archive'''
from fabric.api import local
from datetime import datetime


def do_pack():
    '''function that generates a .tar archive'''
    date = datetime.now().strftime('%Y%m%d%H%M%S')
    archive_name = f'web_static_{date}.tgz'
    try:
        local('mkdir -p versions')
        local(f'tar -czvf versions/{archive_name} web_static')
        return f'versions/{archive_name}'
    except Exception:
        return None
