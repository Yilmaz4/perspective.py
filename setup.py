from setuptools import find_packages, setup

setup(
    name='perspective',
    packages=find_packages(include=['perspective']),
    version='0.1.0',
    description='An easy-to-use API wrapper for Perspective API written in Python.',
    author='Yilmaz04',
    author_email="ymzymz2007@gmail.com",
    license='MIT',
    install_requires=['google-api-python-client', 'pycountry', 'httplib2', 'typing'],
)