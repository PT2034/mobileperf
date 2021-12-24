import subprocess, sys
import shutil,os.path
# DEFAULT_VS = "vs2019"
DEFAULT_SERVER = "10.90.29.33"
DEFAULT_LOCAL_STORAGE_DIR = os.path.abspath(os.path.join(os.path.realpath(__file__), os.pardir))
TMP_BEALOON = True

def execute_system_cmd(this_cmd):
    print("going to run:{}".format(this_cmd))
    p = subprocess.Popen(this_cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    print("stdout: {}".format(out))
    print("stderr: {}".format(err))
    print("return code: {}".format(p.returncode))
    return out, err, p.returncode

def get_download_url(args):
    download_url = "http://{server}/job/PSPlayer_Mac_Build/{build_number}/artifact/builds/{build_number}/v{version}-macx.zip".format(
        server = DEFAULT_SERVER,
        build_number=args[1],
        version=args[2]
    )
    return download_url


def download_by_wget(download_url, local_dir):
    try:
        print("trying to download: {} , put to: {}".format(download_url, local_dir))
        download_cmd = "wget {url} -P {local}".format(url=download_url, local=local_dir)
        out, err, code = execute_system_cmd(download_cmd)
        # normally use below should be ok
        if str(code) != "0":
            print("download file fail")
            global TMP_BEALOON
            TMP_BEALOON = False
            return False

    except Exception as e:
        print(e)
        TMP_BEALOON = False
        return False


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage example: python get_file_from_jk.py 106 2.4.6.0")
        sys.exit(0)
    target_url = get_download_url(sys.argv)
    remote_filename = target_url.split("/")[-1]
    storage_dir = DEFAULT_LOCAL_STORAGE_DIR
    local_path = os.path.join(storage_dir, remote_filename)
    if os.path.isfile(local_path):
        print("{} already exists but continue do download".format(local_path))
    download_by_wget(target_url, storage_dir)
    if TMP_BEALOON:
        filename = "v" + sys.argv[2]
        # if os.path.isfile(os.getcwd().join(filename)):
        if os.path.exists(filename):
            shutil.move(remote_filename, filename)
        else:
            os.mkdir(filename)
            shutil.move(remote_filename, filename)

