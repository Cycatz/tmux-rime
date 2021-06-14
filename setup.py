#!/usr/bin/env python
# coding=utf-8

from setuptools import Extension, find_packages, setup
from setuptools.command.build_py import build_py

name = "tmux_rime"
rime_ext_name = 'rime' 
version = "1.0"


rime_ext = Extension(name='{}._{}'.format(name, rime_ext_name), # SWIG requires _ as a prefix for the module name
                 sources=["lib/rime.i", "lib/rime.c"],
                 libraries=['rime'],
                 extra_compile_args=["-std=c11"],
                 swig_opts=["-outdir", "tmux_rime"])

class BuildPy(build_py):
    def run(self):
        self.run_command('build_ext')
        super(build_py, self).run()
        
setup (name = name,
       version = '0.1',
       author      = "Cycatz",
       description = """A module to use IME in TMUX with Rime""",
       packages        = [name],
       package_dir     = {'tmux_rime': 'tmux_rime'},
       cmdclass = {
            'build_py': BuildPy,
       },
       ext_modules = [rime_ext],
       )
