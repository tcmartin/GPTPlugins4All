from setuptools import setup, find_packages

setup(
    name='gpt-plugins-4all',
    version='1.0.0',
    packages=find_packages(),
    description='GPT Plugins for 4all',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author_email='trevor@zenithai.io',
    install_requires=[
        uuid, json, yaml, requests, openapi_v3_spec_validator, urlencode
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    
)