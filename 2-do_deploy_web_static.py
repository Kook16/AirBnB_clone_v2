#!/usr/bin/python3
'''Fabric script that distributes an archive to my web servers'''
from fabric.api import env, put, sudo
from os.path import exists

env.hosts = ['34.207.155.182', '18.204.14.80']



def do_deploy(archive_path):
    '''Deploy func'''
    if not exists(archive_path):
        return False
    
    # archive_path = /path/to/yor/archive.tar.gz
    try:
        # Upload archive to /tmp/ dir on web server
        put(archive_path, '/tmp/')

        # gets you archive.tar.gz
        filename = archive_path.split('/')[-1]
        # gets you /path/to/your/
        folder_name = filename.split('.')[0]

        release_path = '/data/web_static/releases/' + folder_name

        sudo('mkdir -p {}'.format(release_path))

        sudo('tar -xzf /tmp/{} -C {}'.format(filename, release_path))

        # Delete archive from web server
        sudo('rm /tmp/{}'.format(filename))

        # delete the symbolic link /data/web_static/current
        sudo('rm -f /data/web_static/current')


        # Create a new symbolic link /data/web_static/current

        sudo ('ln -s {} /data/web_static/current'.format(release_path))

        return True
    
    except Exception as e:
        print(e)
        return False
