#!/usr/bin/env python3

import os
import re
import sys
import time
import shutil
import subprocess

biobbs_dir = "/Users/pau/projects/"
bioconda_recipes_dir = "/Users/pau/other_projects/bioconda-recipes"
tmp_dir = "/tmp"
editor_cmd = "atom"
twine_user = "andriopau"
# firefox, safari, chrome...
web_browser_cmd = "open"
conda_skeleton_wait = {'seconds': 5}
dockerfile_wait = {'hours': 2}
singularity_wait = {'hours': 2}

def main(yes_to_all=False):
    print('Welcome to BIOBB new version script.')
    choice = "n"
    while choice.startswith("n"):
        repo = input('Which biobb do you want to release? ')
        repo_path = os.path.join(biobbs_dir, repo)
        print('Path to the code: %s' % repo_path)
        choice = input("Correct ([y]/n)?").lower()

    #Get current version from setup.py
    print("Obtaining version from %s" % os.path.join(repo_path, 'setup.py'))
    ver_current = get_current_version(os.path.join(repo_path, 'setup.py'), replace=False)
    ver_new = get_new_version(ver_current)
    ver_message = 'v'+ver_new+' '+time.strftime('%B %Y')+' Release'
    print("Old version: %s New version: %s Version message: %s")
    if not yes_to_all:
        if input("New version is: %s \n Is it correct ([y]/n)?" % ver_new).lower().startswith('n'):
            ver_new = input('Insert new version value: ')
        if input("New message is: %s \n Is it correct ([y]/n)?").lower().startswith('n'):
            ver_message = input('Insert new version message: ')

    #Modify setup.py
    if yes_to_all or modify_or_open(os.path.join(repo_path, 'setup.py')):
        get_current_version(os.path.join(repo_path, 'setup.py'), replace=True, ver_new=ver_new)

    #Modify docs/source/conf.py with the new version and Message
    if yes_to_all or modify_or_open(os.path.join(repo_path, repo, 'docs', 'source', 'conf.py')):
        pattern_version_conf = re.compile(r"version = u\'.*\'")
        pattern_message_conf = re.compile(r"release = u\'.*\'")
        with open(os.path.join(repo_path, repo, 'docs', 'source', 'conf.py'), 'r+') as conf_file:
            lines = conf_file.readlines()
            for index, line in enumerate(lines):
                if pattern_version_conf.search(line):
                    index_version_conf = index
                if pattern_message_conf.search(line):
                    index_message_conf = index
            lines[index_version_conf] = "version = u'"+ver_new+"'"+'\n'
            lines[index_message_conf] = "release = u'"+ver_message+"'"+'\n'
            conf_file.seek(0)
            conf_file.write("".join(lines))
            conf_file.truncate()

    #Modify Readme.md and docs/README.md
    if yes_to_all or modify_or_open(os.path.join(repo_path, 'README.md')):
        pattern_version_readme = re.compile(r"### Version")
        pattern_copyright_readme = re.compile(r"\* \(c\) 2015-(?P<year>\d\d\d\d)")
        with open(os.path.join(repo_path, 'README.md'), 'r+') as readme_file:
            lines = readme_file.readlines()
            for index, line in enumerate(lines):
                if pattern_version_readme.search(line):
                    index_version_readme = index+1
                if pattern_copyright_readme.search(line):
                    index_copyright_readme = index
                    old_year = pattern_copyright_readme.match(line).groupdict().get('year')
            lines[index_version_readme] = ver_message + '\n'
            lines[index_copyright_readme] = lines[index_copyright_readme].replace(old_year, time.strftime('%Y'))
            lines[index_copyright_readme+1] = lines[index_copyright_readme+1].replace(old_year, time.strftime('%Y'))
            readme_file.seek(0)
            readme_file.write("".join(lines))
            readme_file.truncate()
    if yes_to_all or modify_or_open(os.path.join(repo_path, repo, 'docs', 'source', 'readme.md')):
        shutil.copy2(os.path.join(repo_path, 'README.md'), os.path.join(repo_path, repo, 'docs', 'source', 'readme.md'))

    #Modify the biobb_????.json
    if yes_to_all or modify_or_open(os.path.join(repo_path, repo, 'json_schemas', repo+'.json')):
        pattern_version_json = re.compile(r'"version": "[\d.]+",')
        with open(os.path.join(repo_path, repo, 'json_schemas', repo+'.json'), 'r+') as json_file:
            lines = json_file.readlines()
            for index, line in enumerate(lines):
                if pattern_version_json.search(line):
                    index_version_json = index
                    break
            lines[index_version_json] = '"version": "'+ver_new+'",'+ '\n'
            json_file.seek(0)
            json_file.write("".join(lines))
            json_file.truncate()

    #Push to Github
    if yes_to_all or ask_user("Push to git and create tag"):
        subprocess.run(['git', '-C', repo_path, 'status'])
        subprocess.run(['git', '-C', repo_path, 'add', '.'])
        subprocess.run(['git', '-C', repo_path, 'commit', '-m', ver_message])
        subprocess.run(['git', '-C', repo_path, 'push'])
        subprocess.run(['git', '-C', repo_path, 'push', 'bioexcel'])
        subprocess.run(['git', '-C', repo_path, 'tag', '-a', 'v'+ver_new, ver_message])
        subprocess.run(['git', '-C', repo_path, 'push', 'origin', 'v'+ver_new])
        subprocess.run(['git', '-C', repo_path, 'push', 'bioexcel', 'v'+ver_new])

    #Upload to Pypi
    if yes_to_all or ask_user("Upload to Pypi"):
        subprocess.run(['python3', os.path.join(repo_path, 'setup.py'), os.path.join(repo_path, 'sdist'), os.path.join(repo_path, 'bdist_wheel')])
        cmd = 'python3 -m twine upload '+repo_path+' dist/* <<< '+twine_user
        subprocess.run(cmd, shell=True)

    # Create conda package hash with conda skeleton
    if yes_to_all or ask_user("Create conda package using conda skeleton"):
        skeleton_dir = os.path.join(tmp_dir, repo)
        if os.path.isdir(skeleton_dir):
            shutil.rmtree(skeleton_dir)
        if os.path.isfile(skeleton_dir):
            os.remove(skeleton_dir)
        retval = 1
        while retval != 0:
            print('Waiting for Pypi version to be updated')
            countdown(**conda_skeleton_wait)
            retval = subprocess.run(['conda', 'skeleton', 'pypi', repo, '--version', ver_new, '--output-dir', tmp_dir])

        # Get the hash value from the conda skeleton recipe
        pattern_hash_value = re.compile(r"{% set hash_value = \"(?P<hash_value>\w+)\" %}")
        skeleton_meta = os.path.join(skeleton_dir, 'meta.yaml')
        with open(skeleton_meta, 'r') as skeleton_file:
            for line in skeleton_file:
                match = pattern_hash_value.match(line)
                if match:
                    hash_value = match.group('hash_value')
                    break
    else:
        hash_value = input("New meta.yaml hash_value: ")

    # Updating Bioconda repository and creating a new branch
    if yes_to_all or ask_user("Update bioconda repository and create a new branch"):
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'checkout', '-f', 'master'])
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'pull', 'origin', 'master'])
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'branch', '-D', repo])
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'push', 'origin', '--delete', repo])
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'checkout', '-b', repo])

    # Modify Bioconda recipe adding the correct version and  hash_value
    if yes_to_all or modify_or_open(os.path.join(bioconda_recipes_dir, 'recipes', 'meta.yaml')):
        with open(os.path.join(bioconda_recipes_dir, 'recipes', 'meta.yaml'), 'r+') as meta_file:
            pattern_version_meta = re.compile(r"{% set version = \"(?P<version>[\d.]+)\" %}")
            lines = meta_file.readlines()
            for index, line in enumerate(lines):
                if pattern_version_meta.match(line):
                    index_version_meta = index
                if pattern_hash_value.match(line):
                    index_hash_value = index
            lines[index_version_meta] = '{% set version = "'+ver_new+'" %}' + '\n'
            lines[index_hash_value] = '{% set hash_value = "'+hash_value+'" %}' + '\n'
            meta_file.seek(0)
            meta_file.write("".join(lines))
            meta_file.truncate()

#Ask to open build.sh
#Ask to open post-link.sh


    # Create pull request in bioconda repository
    if yes_to_all or ask_user("Create bioconda pull request"):
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'status'])
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'commit', '-m', ver_message])
        subprocess.run(['git', '-C', bioconda_recipes_dir, 'push', '-u', 'origin', repo])
        subprocess.run([web_browser_cmd, "https://github.com/bioconda/bioconda-recipes/pull/new/"+repo])

    # Modify Dockerfile if exists
    dockerfile_path = os.path.join(repo_path, 'Dockerfile')
    if os.path.exists(dockerfile_path):
        if yes_to_all or modify_or_open(dockerfile_path):
            with open(dockerfile_path, 'r+') as dockerfile:
                pattern_version_docker = re.compile("RUN conda install -y "+repo+r"==[\d\.]+")
                lines = meta_file.readlines()
                for index, line in enumerate(lines):
                    if pattern_version_docker.search(line):
                        index_version_docker = index
                lines[index_version_docker] = "RUN conda install -y "+repo+"=="+ver_new+ "\n"
                dockerfile.seek(0)
                dockerfile.write("".join(lines))
                dockerfile.truncate()

        if yes_to_all or ask_user("Wait and push changes?"):
            countdown(**dockerfile_wait)
            subprocess.run(['git', '-C', repo_path, 'status'])
            subprocess.run(['git', '-C', repo_path, 'add', '.'])
            subprocess.run(['git', '-C', repo_path, 'commit', '-m', ver_message])
            subprocess.run(['git', '-C', repo_path, 'push'])
            subprocess.run(['git', '-C', repo_path, 'push', 'bioexcel'])

    # Modify singularity
    singularity_path = os.path.join(repo_path, 'Singularity.latest')
    if yes_to_all or modify_or_open(singularity_path):
        if os.path.exists(dockerfile_path):
            with open(singularity_path, 'r+') as singularity_file:
                lines = meta_file.readlines()
                if lines[0].startswith('#'):
                    lines[0] = "# "+ver_new+"\n"
                else:
                    lines.insert(0, "# "+ver_new+"\n")
                singularity_file.seek(0)
                singularity_file.write("".join(lines))
                singularity_file.truncate()
        else:
            with open(dockerfile_path, 'r+') as dockerfile:
                pattern_version_singularity = re.compile("From: "+repo+":"+r"[\d\.]+")
                lines = meta_file.readlines()
                for index, line in enumerate(lines):
                    if pattern_version_singularity.search(line):
                        index_version_singularity = index
                lines[index_version_singularity] = "From: "+repo+":"+ver_new+"--py_0"+"\n"
                singularity_file.seek(0)
                singularity_file.write("".join(lines))
                singularity_file.truncate()
    if yes_to_all or ask_user("Wait and push changes?"):
        countdown(hours=2)
        subprocess.run(['git', '-C', repo_path, 'status'])
        subprocess.run(['git', '-C', repo_path, 'add', '.'])
        subprocess.run(['git', '-C', repo_path, 'commit', '-m', ver_message])
        subprocess.run(['git', '-C', repo_path, 'push'])
        subprocess.run(['git', '-C', repo_path, 'push', 'bioexcel'])

def countdown(seconds=0, minutes=0, hours=0):
    seconds_left = seconds+(minutes*60)+(hours*3600)
    while seconds_left:
        minu, sec = divmod(seconds_left, 60)
        hour, minu = divmod(minu, 60)
        time_str = '{:02d}:{:02d}:{:02d}'.format(hour, minu, sec)
        print(time_str, end='\r')
        time.sleep(1)
        seconds_left -= 1

def modify_or_open(file_to_open):
    choice = ""
    while choice not in ["y", "n", "o"]:
        choice = input("Modify %s [y]es/no/open it (I'll do it myself)?" % file_to_open).lower()
        if choice.startswith("n"):
            return False
        if choice.startswith("y"):
            return True
        if choice.startswith("o"):
            subprocess.run([editor_cmd, file_to_open])
            input("Waiting... Press any key to continue")
            return False

def ask_user(message):
    if input(message + " ([y]/n)?").lower().startswith('n'):
        input("Waiting... Press any key to continue")
        return False
    return True

def get_current_version(setuppy_path, replace=True, ver_new=None):
    pattern = re.compile(r"version\s*=\s*\"(?P<ver>\d\.\d\.\d)\"\s*,")
    with open(setuppy_path, 'r+') as setup_file:
        lines = setup_file.readlines()
        for index, line in enumerate(lines):
            if pattern.search(line):
                ver_current = pattern.match(line).groupdict().get('ver')
                if not replace:
                    return ver_current
                break
        if not ver_new:
            ver_new = get_new_version(ver_current)
        lines[index] = 'version="'+ver_new+'",\n'
        setup_file.seek(0)
        setup_file.write("".join(lines))
        setup_file.truncate()
        return ver_current

def get_new_version(version_str):
    ver_new = list(int(version_str.replace('.', ''))+1).insert(-1, '.')
    return str(ver_new.insert(-3, '.'))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1].startswith("-y"):
            main(yes_to_all=True)
    else:
        main()
