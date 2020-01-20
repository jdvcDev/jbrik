from setuptools import setup

setup(
    name='jbrik',
    version='1.0',
    packages=['utils', 'motor_core', 'solver_core', 'tracker_core', 'tracker_core.tracker', 'tracker_core.resolver',
              'tracker_core.resolver.colortools'],
    url='',
    license='',
    author='jdvcDev',
    author_email='',
    description='',
    install_requires=[
        'numpy',
        'opencv-python',
        'webcolors'


    ]
)
