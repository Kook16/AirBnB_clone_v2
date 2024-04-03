#!/usr/bin/python3
"""
distributes an archive to your web servers
"""
from os import path
from datetime import datetime
from fabric.api import local
from fabric.api import env, run, put, task


env.hosts = ['54.174.69.148', '18.204.20.114']


@task
def do_pack():
    """
    function that generates a .tar archive
    """
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    arch_name = "web_static_{}.tgz".format(date)
    try:
        local('mkdir -p versions')
        local('tar -cvzf versions/{} web_static'.format(arch_name))
        return "versions/{}".format(arch_name)
    except Exception:
        return None


@task
def do_deploy(archive_path):
    """
    Deploy function
    """
    if not path.exists(archive_path):
        return False
    try:

        arch_tgz = archive_path.split('/')[-1]
        arch = arch_tgz.split('.')[0]
        arch_dir = '/data/web_static/releases/{}/'.format(arch)

        put(archive_path, '/tmp/')
        run('mkdir -p {}'.format(arch_dir))
        run('tar -xzf /tmp/{} -C {}'.format(arch_tgz, arch_dir))
        run('rm /tmp/{}'.format(arch_tgz))
        run('sudo mv {}web_static/* {}'.format(arch_dir, arch_dir))
        run('rm -rf {}web_static'.format(arch_dir))
        run('rm -rf /data/web_static/current')
        run('ln -s {} /data/web_static/current'.format(arch_dir))

        print('New version deployed!')
        return True

    except Exception as e:
        print(e)
        return False


@task
def deploy():
    """
    Create and distribute an archive to web server
    """
    try:
        archive_path = do_pack()
        if archive_path is None:
            return False
        return do_deploy(archive_path)
    except Exception:
        return False
