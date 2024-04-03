#!/usr/bin/python3
'''Fabric script that distributes an archive to my web servers'''
from fabric.api import env, put, sudo, run
from os import path
env.hosts = ['54.174.69.148', '18.204.20.114']


def do_deploy(archive_path):
    '''Deploy func'''
    if not path.isfile(archive_path):
        return False
    try:

        arch_tgz = archive_path.split("/")[-1]
        arch = arch_tgz.split(".")[0]
        # arch_dir = "/data/web_static/releases/{}/".format(arch)
        arch_dir = '/data/web_static/releases/' + arch + '/'

        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(arch_dir))
        run("sudo tar -xzf /tmp/{} -C {}".format(arch_tgz, arch_dir))
        run("sudo rm /tmp/{}".format(arch_tgz))
        run("sudo mv {}web_static/* {}".format(arch_dir, arch_dir))
        run("sudo rm -rf {}web_static".format(arch_dir))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(arch_dir))

        print("New version deployed!")
        return True

    except Exception:
        return False
