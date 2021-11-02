from setuptools import setup
import json


with open('metadata.json', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_oskolskayatungusic',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_oskolskayatungusic'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'oskolskayatungusic=lexibank_oskolskayatungusic:Dataset',
        ]
    },
    install_requires=[
        'pylexibank>=3.1.0',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
