from setuptools import setup, find_packages

setup(
    name='rbns-downloader',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rbns=rbns_downloader:main',
        ],
    },
    install_requires=[
        'requests',
		'jellyfish',
		'clint',
    ],
    author='Francisco Fernando Cavazos',
    author_email='ffcavazos@miners.utep.edu',
    description='A package to download RNA Bind-n-Seq experimental data',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Ferny730JR/rbns_downloader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
