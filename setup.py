from setuptools import setup, find_packages

setup(
    name='GPTPlugins4All',
    version='1.0.2',
    packages=find_packages(),
    description='GPT Plugins for 4all',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author_email='trevor@zenithai.io',
    url='https://github.com/tcmartin/gpt-plugins-4all',
    install_requires=[
        'PyYAML', 'requests', 'openapi-spec-validator'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'gpt-plugins-4all=GPTPlugins4All.cli:main',  # "gpt-plugins-4all" is the command users will type
        ],
    },
)
