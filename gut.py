#!/usr/bin/python3

import sys
import subprocess
import pprint

def query_yes_no(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def get_branch_list(remote = False):
    args = ['git', 'branch']
    if remote:
        args = ['git', 'branch', '-r']
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    branches = proc.stdout.read()
    branches = branches.decode('ascii').split("\n")
    return map(lambda x: x.replace('*', '').strip(), branches)

def has_branch(branch_name, remote = False):
    branches = get_branch_list(remote)
    for branch in branches:
        if branch == branch_name:
            return True
    return False

def stash_changes():
    args = ['git', 'stash']
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    result = proc.stdout.read().decode('ascii')
    return 'No local changes' not in result

def get_current_branch():
    proc = subprocess.Popen(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stdout=subprocess.PIPE)
    branch = proc.stdout.read()
    return branch.decode('ascii').strip()

if len(sys.argv) > 1:
    if sys.argv[1] in ['retreat', 'ret']:
        if len(sys.argv) > 2:
            subprocess.call(['git', 'checkout', sys.argv[2]])
        else:
            subprocess.call(['git', 'stash'])
            subprocess.call(['git', 'reset', 'HEAD'])
    elif sys.argv[1] in ['switch', 'sw'] and len(sys.argv) > 2:
        if has_branch(sys.argv[2]):
            subprocess.call(['git', 'checkout', sys.argv[2]])
        else:
            subprocess.call(['git', 'checkout', '-b', sys.argv[2]])
    elif sys.argv[1] in ['sync', 'sy']:
        branch = get_current_branch()
        if has_branch('origin/' + branch, True):
            stashed = stash_changes()
            subprocess.call(['git', 'pull'])
            if stashed:
                subprocess.call(['git', 'stash', 'pop'])
            subprocess.call(['git', 'push'])
        else:
            if query_yes_no("The branch " + branch + " doesn't exist on the remote. Create it?"):
                subprocess.call(['git', 'push', '--set-upstream', 'origin', branch])
            else:
                print("Giving up.")
    else:
        args = sys.argv[1:]
        args.insert(0, 'git')
        retcode = subprocess.call(args)
        exit(retcode)
else:
    exit(subprocess.call(['git']))
