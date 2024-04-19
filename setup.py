#!/usr/bin/env python
import setuptools

try:
    with open('README.md', 'r', encoding='utf-8') as fh:
        long_description = fh.read()
except (IOError, OSError):
    long_description = ''

setuptools.setup(
    name='xunter',
    version='0.2.0',
    license='MIT',
    author='anki-code',
    author_email='no@no.no',
    description="Profiling for the xonsh shell based on hunter.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    install_requires=['xonsh', 'hunter'],
    py_modules=["xunter"],
    scripts=['xunter', 'xunter2excel'],
    platforms='any',
    url='https://github.com/anki-code/xunter',
    project_urls={
        "Documentation": "https://github.com/anki-code/xunter/blob/master/README.md",
        "Code": "https://github.com/anki-code/xunter",
        "Issue tracker": "https://github.com/anki-code/xunter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Shells",
        "Topic :: System :: System Shells",
        "Topic :: Terminals",
    ]
)
