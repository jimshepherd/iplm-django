from setuptools import setup

setup(
    name='iplm',
    version='0.1',
    packages=['iplm', 'iplm_graphql', 'iplm_graphql.migrations'],
    url='',
    license='MIT',
    author='Jim Shepherd',
    author_email='jeshep@gmail.com',
    description='Item-Process Lifecycle Management',
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
        'feincms3',  # For displaying trees in admin
        'django-currentuser',  # Add current user to Tracker models
        'django-sortedm2m',  # Ordered many-to-many
        'xlsxwriter', # Parses Excel spreadsheets on upload
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
    dependency_links=[
      'https://github.com/PaesslerAG/django-currentuser/tarball/master#egg=django-currentuser'
    ],
)
