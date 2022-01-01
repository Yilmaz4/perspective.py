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
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)