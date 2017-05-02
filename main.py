# -*- coding:utf-8 -*-

import os
import sys
import fileinput
import time


class print_colors:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_info(info):
    print print_colors.OKGREEN + info + print_colors.ENDC


def print_fail(info):
    print print_colors.FAIL + info + print_colors.ENDC


def print_warn(info):
    print print_colors.WARNING + info + print_colors.ENDC


def replace_all_file_content(project_dir, find, replace):
    for (parent, dirnames, filenames) in os.walk(project_dir):
        for filename in filenames:
            filepath = os.path.join(parent, filename)
            print 'parent path = ', parent
            print 'file path = ', filepath
            replace_file_content(filepath=filepath, find=find, replace=replace)


def replace_all_dir(project_dir, find, replace):
    # #topdown决定遍历的顺序，如果topdown为True，则先列举top下的目录，然后是目录的目录，依次类推
    for (parent, dirnames, filenames) in os.walk(project_dir, topdown=False):
        for dirname in dirnames:
            if find in dirname:
                src = os.path.join(parent, dirname)
                dst_dirname = str.replace(dirname, find, replace)
                dst = os.path.join(parent, dst_dirname)
                print 'dir rename ', src, '---->', dst
                os.rename(src, dst)


def replace_all_file(project_dir, find, replace):
    # #topdown决定遍历的顺序，如果topdown为True，则先列举top下的目录，然后是目录的目录，依次类推
    for (parent, dirnames, filenames) in os.walk(project_dir, topdown=False):
        for filename in filenames:
            if find in filename:
                src = os.path.join(parent, filename)
                dst_filename = str.replace(filename, find, replace)
                dst = os.path.join(parent, dst_filename)
                print 'file rename ', src, '---->', dst
                os.rename(src, dst)


def replace_file_content(filepath=None, find=None, replace=None):
    if filepath is None:
        print_warn('file is none, return')
        return

    if find is None:
        print_warn('find is none, return')
        return

    if replace is None:
        print_warn('replace is none, return')
        return

    for line in fileinput.input(filepath, inplace=1):
        if find in line:
            line = line.replace(find, replace)
        sys.stdout.write(line)


def input_content(prompt=None):
    content = raw_input(prompt)
    content = content.strip()
    if len(content) == 0:
        content = None
    return content


if __name__ == '__main__':

    if os.path.exists('fast-template'):
        print_warn('fast-template dir exists, exit. please change it')
        exit(1)

    # 项目名
    p_name = None
    while p_name is None:
        p_name = input_content('Enter your project name :')

    # bundle identifier
    app_identifier = None
    while app_identifier is None:
        app_identifier = input_content('Enter your app bundle identifier :')

    if os.path.exists(p_name):
        print_warn('project ' + p_name + ' exists, please change it')
        exit(1)

    print '================================================'
    print 'projext_name      = ', p_name
    print 'bundle identifier = ', app_identifier
    print '================================================'

    if p_name is None:
        print_fail('error: project name is none.')
        exit(1)

    if app_identifier is None:
        print_fail('error: bundle identifier is none.')
        exit(1)

    print 'p_name = ', p_name
    print 'app_identifier = ', app_identifier

    temp_dst = 'temp_dst_' + str(time.time().real)
    template_name = 'fast-template'
    template_config_name = 'fast_template'

    os.system('git clone https://github.com/lingyfh/fast-template.git')
    os.system('mkdir ' + temp_dst)
    os.system('cp -rf fast-template/fast-template ' + temp_dst)

    # 修改bundle identifier
    replace_all_file_content(temp_dst, 'com.lingyfh.fast-template', app_identifier)

    # 修改所有配置中的fast-template, fast_template
    replace_all_file_content(temp_dst, template_name, p_name)
    replace_all_file_content(temp_dst, template_config_name, p_name)

    # 修改所有fast-template文件名字
    replace_all_file(temp_dst, template_name, p_name)

    # 修改所有fast-template目录名字
    replace_all_dir(temp_dst, template_name, p_name)

    # 将目标项目当到当前目录下,并删除中间生成的文件
    os.system('mkdir ' + p_name)
    os.system('mv ' + temp_dst + '/' + p_name + ' .')
    os.system('cd ' + p_name + ' && pod install')
    os.system('rm -rf ' + temp_dst)
    os.system('rm -rf ' + template_name)

    print_info('success create project :' + p_name)
