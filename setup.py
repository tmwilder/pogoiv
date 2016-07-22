from setuptools import setup

setup(
    name='pogoiv',
    version='1.0.0',
    description='Library for calculating possible pokemon GO IVs.',
    url='http://github.com/tmwilder/pogoiv',
    author='Tim Wilder',
    author_email='tmwilder@gmail.com',
    license='MIT',
    packages=['pogoiv'],
    package_dir={'pogoiv': 'pogoiv'},
    package_data={'pogoiv': ['data/*.tsv']},
    test_suite='nose.collector',
    tests_require=['nose'],
    zip_safe=False
)