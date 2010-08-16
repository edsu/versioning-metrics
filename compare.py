#!/usr/bin/env python

"""
Create a directory called 'data', populate it with some content, and this 
script will use it to compare some revision control systems from the 
perspective of repository size and the time it takes to do commit operations.

This script expects git, mercurial and dflat to be installed. It also 
requires that you be on a Unix system of some flavor.
"""

import os
import shutil
import datetime

def main():
    setup()

    print
    print "create repository times"
    msg("git", t(create_git))
    msg("hg", t(create_hg))
    msg("dflat", t(create_dflat))

    print
    print "repository size"
    msg("git", du("git/.git"))
    msg("hg", du("hg/.hg"))
    msg("dflat", du("dflat", ignore_dirs=["v002"]))

    print
    print "checkout sizes"
    msg("git", du("git"))
    msg("hg", du("hg"))
    msg("dflat", du("dflat"))

    print
    print "commit changes"
    modify_files("git")
    msg("git", t(modify_git))
    modify_files("hg")
    msg("hg", t(modify_hg))
    modify_files("dflat/v002")
    msg("dflat", t(modify_dflat))

    print
    print "repository sizes after commit"
    msg("git", du("git/.git"))
    msg("hg", du("hg/.hg"))
    msg("dflat", du("dflat"))

def msg(k, v):
    print "%-10s %s" % (k, v)

def t(f):
    t1 = datetime.datetime.now()
    f()
    t2 = datetime.datetime.now()
    return t2 - t1

def du(d, ignore_dirs=[]):
    bytes = 0
    for dirpath, dirnames, filenames in os.walk(d):
        for dirname in dirnames:
            if dirname in ignore_dirs:
                dirnames.remove(dirname)
        else:
            for filename in filenames:
                bytes += os.stat(os.path.join(dirpath, filename)).st_size
    return bytes

def setup():
    shutil.rmtree("git", ignore_errors=True)
    shutil.copytree("data", "git")
    shutil.rmtree("hg", ignore_errors=True)
    shutil.copytree("data", "hg")
    shutil.rmtree("dflat", ignore_errors=True)
    shutil.copytree("data", "dflat")

def create_git():
    os.chdir("git")
    os.system("git init > /dev/null")
    os.system("git add *")
    os.system("git commit -a -m 'initial commit' > /dev/null")
    os.chdir("..")

def create_hg():
    os.chdir("hg")
    os.system("hg init")
    os.system("hg add -q * 2>/dev/null")
    os.system("hg commit -m 'initial commit'")
    os.chdir("..")

def create_dflat():
    os.chdir("dflat")
    os.system("dflat init")
    os.system("dflat checkout > /dev/null")
    os.chdir("..")

def modify_git():
    os.chdir("git")
    os.system("git commit -a -m 'modified files' > /dev/null")
    os.chdir("..")

def modify_hg():
    os.chdir("hg")
    os.system("hg commit -m 'modified files'")
    os.chdir("..")

def modify_dflat():
    os.chdir("dflat")
    os.system("dflat commit > /dev/null")
    os.chdir("..")

def modify_files(directory):
    # add a space to every file in a directory
    for dirpath, dirnames, filenames in os.walk(directory):
        # don't walk around inside directories that start with .
        for dirname in dirnames:
            if dirname.startswith('.'):
                dirnames.remove(dirname)
        for filename in filenames:
            open(os.path.join(dirpath, filename), 'w').write(" ")

if __name__ == '__main__':
    main()
