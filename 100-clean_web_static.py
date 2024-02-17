#!/usr/bin/python3
"""
Deltes out-date archives
"""
from os import path
from datetime import datetime
from fabric.api import local
from fabric.api import env, run, put, task


env.hosts = ['34.207.155.182', '18.204.14.80']


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

@task
def do_clean(number=0):
    '''deletes out-of-date archives

    Args:
        number (int, optional): number is the number of archives, including 
         the most recent, to keep

       Default to 0
       if number is 0 or 1, keep only the most recent version of your archiv       if number is 2, keep the most recent and second most recent versions of your archive
    '''
    num = 1

    try:
        num = int(number)
    except ValueError:
        pass

    # local dir clean up
    local_version_directory = "versions"
    if num in (0, 1):
        local("cd {} && ls -t | head -n -1 | sudo xargs rm -rf"
              .format(local_version_directory, num))
    elif num >= 2:
        local("cd {} && ls -t | head -n -{} | sudo xargs rm -fr"
              .format(local_version_directory, num))

    remote_version_directory = "/data/web_static/releases/*"
    run("ls -dt {} | head -n -{} | xargs rm -fr"
        .format(remote_version_dir, num))
