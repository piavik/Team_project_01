from setuptools import setup, find_namespace_packages

setup(
    name='team-project-01',
    version='0.6.1',
    description='ClI Assistant',
    url='https://github.com/piavik/team-project-01',
    author='project-group4',
    license='MIT',
    packages=find_namespace_packages(),
    install_requires=['prompt_toolkit'],
    include_package_data=True,
    entry_points={'console_scripts': ['Informator = team-project-01.main:main']}
)
