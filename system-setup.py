#!/usr/bin/env python2

import sys
import os
import argparse

ROOT = HERE = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(ROOT, "deps/readies"))
import paella

#----------------------------------------------------------------------------------------------

class RedisJSONSetup(paella.Setup):
    def __init__(self, nop=False):
        paella.Setup.__init__(self, nop)

    def common_first(self):
        self.setup_pip()
        self.pip_install("wheel")
        self.pip_install("setuptools --upgrade")

        self.install("git wget clang cmake")

    def debian_compat(self):
        self.install("build-essential")
        self.install("python-psutil")

    def redhat_compat(self):
        self.install("redhat-lsb-core")
        self.install("epel-release")
        self.group_install("'Development Tools'")
        self.install("python2-psutil")

    def fedora(self):
        self.group_install("'Development Tools'")

    def macosx(self):
        if sh('xcode-select -p') == '':
            fatal("Xcode tools are not installed. Please run xcode-select --install.")

    def common_last(self):
        # redis-py-cluster should be installed from git due to redis-py dependency
        self.run("python2 -m pip uninstall -y -q redis redis-py-cluster ramp-packer RLTest semantic-version")
        self.pip_install("--no-cache-dir git+https://github.com/Grokzen/redis-py-cluster.git@master")
        # self.pip_install("--no-cache-dir git+https://github.com/RedisLabsModules/RLTest.git@master")
        self.pip_install("--no-cache-dir git+https://github.com/RedisLabs/RAMP@master")
        
        self.pip_install("awscli")

        self.pip_install("-r %s/deps/readies/paella/requirements.txt" % ROOT)
        self.pip_install("-r %s/test/pytest/requirements.txt" % ROOT)
        
#----------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser(description='Set up system for build.')
parser.add_argument('-n', '--nop', action="store_true", help='no operation')
args = parser.parse_args()

RedisJSONSetup(nop = args.nop).setup()
