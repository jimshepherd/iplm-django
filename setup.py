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
        'django-treebeard',  # Tree models
        'psycopg2',
        'graphene-django',
        'PyJWT==1.7.1',  # Solves 'str' object has no attribute 'decode'
        'django-graphql-jwt',
        'django-cors-headers',
        'django-environ',  # Handles secrets stored in .env files
    ],
    extras_require={
        'test': [
            'coverage',
        ],
        'deploy': [
            'daphne',
        ]
    },
)
