from setuptools import setup

setup(
    name='mpd_django',
    version='0.1',
    packages=['mpd_django', 'mpd_graphql', 'mpd_graphql.migrations'],
    url='',
    license='MIT',
    author='Jim Shepherd',
    author_email='jeshep@gmail.com',
    description='Material and process data',
    python_requires='>=3.6',
    install_requires=[
        'Django',
        'django-tree-queries',  # Tree models
        'psycopg2',
        'graphene-django==3.0.0b7',  # 3.0+ required for Django 4
        'PyJWT',
        'django-graphql-jwt',
        'django-cors-headers',
        'django-environ',  # Handles secrets stored in .env files
    ],
    extras_require={
        'test': [
            'coverage',
            'mixer',
        ],
        'deploy': [
            'daphne',
        ]
    },
)
