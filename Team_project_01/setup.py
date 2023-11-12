from setuptools import setup, find_namespace_packages

setup(
    name='Team_project_01',
    version='0.1.0',
    description='ClI Assistant',
    url='https://github.com/piavik/Team_project_01',
    author='project-group4',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['prompt_toolkit'],
    entry_points={'console_scripts': ['botik = Team_project_01.main:main']}
)