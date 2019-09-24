from setuptools import setup

setup(
    name='gloop',
    version='',
    packages=['gloop', 'gloop.web', 'gloop.web.views', 'gloop.entities', 'gloop.use_cases', 'gloop.repositories',
              'gloop.repositories.schemas'],
    url='',
    license='',
    author='Arthur Pitzer',
    author_email='',
    description='',
    install_requires=[
        'aiohttp',
        'aiohttp_cors',
        'motor',
        'bcrypt'
    ]
)
