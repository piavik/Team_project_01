from setuptools import setup, find_namespace_packages

setup(
    name='Team_project_01',
    version='0.5.4',
    description='ClI Assistant',
    url='https://github.com/piavik/Team_project_01',
    author='project-group4',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['prompt_toolkit'],
    include_package_data=True,
    entry_points={'console_scripts': ['Informator = Team_project_01.main:main']}
)
