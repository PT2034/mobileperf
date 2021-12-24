from Dcmd import execute_command as exsh
from Dcmd import execute_pipeline_command

client_build_jenkins_ws = '/Users/tipaipai/jenkins_workspace/workspace/client_build/'


def sync_apk_to_git_server():
    pass

def prepare_latest_apk():
    client_build_jenkins_ws = '/Users/larryzhu/PycharmProjects/zantao_tools/sample/pdir/'
    apk_dispatcher_dir = client_build_jenkins_ws + 'genie_apk_list'

    generic_apk_dir = apk_dispatcher_dir + '/timestamp/'
    generic_commit_log_name = generic_apk_dir + 'commit.log'

    exsh('mkdir -p ' + generic_apk_dir)
    exsh('touch ' + generic_commit_log_name)
    ## genie setting specific script

    # exsh('touch '+curr_log)
    curr_commit_file_path = generic_apk_dir + 'genie_setting_commit.log'
    curr_apk_file_path = generic_apk_dir + 'genie_setting_apk.log'
    temp_apk_file_path = generic_apk_dir + 'genie_setting_apk_temp.log'
    exsh('touch ' + curr_commit_file_path)
    exsh('touch ' + curr_apk_file_path)

    # run on jenkins job
    # exsh('echo genie_setting > /Users/larryzhu/PycharmProjects/zantao_tools/sample/pdir/genie_apk_list/timestamp/genie_setting_commit.log')
    # exsh('less '+curr_commit_file_path)
    # exsh('echo app/build/outputs/apk/debug/genie_setting_0.1.0_28_210913_180519_107_9288bb3_debug.apk>'+curr_apk_file_path)
    # exsh('less '+curr_apk_file_path)

    # py commands
    genie_setting_working_dir = client_build_jenkins_ws + '/智能学习-设置/babymonkey_setting/'
    genie_setting_working_dir = generic_apk_dir
    # exsh('cd ' + genie_setting_working_dir)
    print("start here...")
    execute_pipeline_command('cat ' + curr_apk_file_path)
    # execute_pipeline_command('cat '+curr_commit_file_path+' > ' + generic_commit_log_name)
    concat_apk_full_path = 'cat ' + curr_apk_file_path + '| awk \'{print \"' + genie_setting_working_dir + '\"$1}\' >' + temp_apk_file_path
    print('concat_apk_full_path=\n', concat_apk_full_path)
    # execute_pipeline_command(concat_apk_full_path)
    execute_pipeline_command('cat ' + temp_apk_file_path)

    # apk_dir = 'cat ' + temp_apk_file_path + '| rev | cut -d/ -f1 | rev |xargs -I file mv file ' + generic_apk_dir
    apk_dir = 'cat ' + temp_apk_file_path + '| xargs -I file mv file ' + generic_apk_dir + 'a.apk'
    print("apk_dir=\n", apk_dir)
    execute_pipeline_command(apk_dir)


prepare_latest_apk()
sync_apk_to_git_server()


if __name__ == '__main__':
    client_build_jenkins_ws = '/Users/tipaipai/jenkins_workspace/workspace/client_build'
    # print(execute_command('ls'))
