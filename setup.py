import uuid
from setuptools import setup
from pip.req import parse_requirements


# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = parse_requirements('pip_requirements.txt', session=uuid.uuid1())


setup(
    name='Lyvi',
    version='2.0-git',
    description='Command-line lyrics (and more!) viewer',
    long_description=open('README.rst').read(),
    url='http://ok100.github.io/lyvi/',
    author='Ondrej Kipila',
    author_email='ok100@openmailbox.org',
    license='WTFPL',
    packages=['lyvi', 'lyvi.players'],
    entry_points={
        'console_scripts': [
            'lyvi = lyvi:main'
        ]
    },
    install_requires=[str(ir.req) for ir in install_reqs],
    package_data={'lyvi': ['data/pianobar/*']},
    data_files=[('share/man/man1', ['doc/lyvi.1'])]
)

print('To enable MPRIS support, please make sure to have python-dbus and python-gobject modules installed.')
