import shlex
from subprocess import Popen, PIPE

def run():
    containers = get_exited_containers()
    print('number containers: {}'.format(len(containers)))
    for container in containers:
        print('\t* deleting container: {}'.format(container))
        delete_container(container)
    print("")
    delete_images_no_used()

def get_exitcode_stdout_stderr(cmd):
    args = shlex.split(cmd)

    proc = Popen( args, stdout=PIPE, stderr=PIPE )
    out, err = proc.communicate()
    exitcode = proc.returncode

    return exitcode, out, err

def get_exited_containers():
    cmd = "docker ps -q -f status=exited"

    print("get containers with status exited")
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    return out.splitlines()

def delete_container(container):
    cmd = "docker rm {}".format(container)
    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    print("\t\t* exitcode: {}".format(exitcode))

def delete_images_no_used():
    print("deleting images no used...")
    cmd = "docker images -f dangling=true -q"

    exitcode, out, err = get_exitcode_stdout_stderr(cmd)
    images = out.splitlines()
    if len( images ) > 0:
        for image in images:
            print('deleting image: {}'.format(image) )
            cmd = "docker rmi {}".format(image)

            i_exitcode, i_out, i_err = get_exitcode_stdout_stderr(cmd)
            print("\t\t* exitcode: {}".format(i_exitcode))
            print( "\t\t* error: {}".format(err) )
    
    print("...")
    print("end process")

if __name__== "__main__":
    run()