from setuptools import setup, find_packages

setup(
    name='GPTPlugins4All',
    version='1.0.5',
    packages=find_packages(),
    description='GPT Plugins for 4all',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author_email='trevor@gptplugins4all.com',
    url='https://github.com/DataStreams-Solutions/GPTPlugins4All',
    project_urls={
        "Bug Tracker": "https://github.com/DataStreams-Solutions/GPTPlugins4All/issues",
        "Documentation": "https://github.com/DataStreams-Solutions/GPTPlugins4All#readme",
        "Source Code": "https://github.com/DataStreams-Solutions/GPTPlugins4All",
    },
    install_requires=[
        'PyYAML', 'requests', 'openapi-spec-validator'
    ],
    extras_require={
        'openai':  ["openai"]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'gpt-plugins-4all=GPTPlugins4All.cli:main',
        ],
    },
)
