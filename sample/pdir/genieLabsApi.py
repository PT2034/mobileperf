import gitlab
from tools import tool

url = 'https://git.100tal.com/'  # gitlab安装地址
private_token = 'WRxwhMCyTjRjNE9zP4z2'  # gitlab 就是上面我们获取的那个

'''
    condition={
        'project_id':'id1'
        'branche_name':'name'
        'begin_time':'' #代表无
        'end_time':'' #代表无
    }
'''

def get_code_quantity_by_condition(condition):
    gl = gitlab.Gitlab(url, private_token)
    project_id = condition['project_id']
    project = gl.projects.get(project_id)
    print('获取项目完成')
    branche_name = condition['branche_name']
    # branches = project.branches.get(branche_name)
    # print('获取分支列表完成')
    '''
    代码量的统计规则
    在指定项目的指定分支内所有或一段时间内的所有commit 
    将commit中的新增代码行数，删减代码行数和总修改代码行数分别累加得到代码量
    '''
    query_parameter = {
        'ref_name': branche_name
    }
    if condition['begin_time'] != '#':
        query_parameter['since'] = condition['begin_time']
    if condition['end_time'] != '#':
        query_parameter['until'] = condition['end_time']

    additions = 0
    deletions = 0
    total = 0
    name_list = []
    d = {}
    commits = project.commits.list(all=True, query_parameters=query_parameter)  # 根据时间、分支名遍历该分支下面所有的提交记录
    for commit in commits:  # 然后再遍历每个提交记录，查询每个提交记录的人和量
        name_list.append({commit.author_name: commit.id})
        d[commit.author_name] = 0

    for j in d:
        total = 0
        for i in name_list:
            if list(i.keys())[0] == j:
                com = project.commits.get(list(i.values())[0])
                total += com.stats['total']
                d.update({j: total})

    return d


if __name__ == '__main__':
    condition = {
        'project_id': '27912',
        'branche_name': 'dev',
        'begin_time': '#',
        'end_time': '#'
    }

    print(get_code_quantity_by_condition(condition))