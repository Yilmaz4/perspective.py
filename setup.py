from setuptools import find_packages, setup

with open("README.md", encoding="utf-8", mode="r") as file:
    long_desc = file.read()
setup(
    name='perspective.py',
    packages=find_packages(include=['perspective']),
    version='0.3.3',
    description='An easy-to-use API wrapper for Perspective API written in Python.',
    long_description=long_desc,
    author='Yilmaz04',
    author_email="ymzymz2007@gmail.com",
    license='MIT',
    install_requires=['google-api-python-client', 'pycountry', 'httplib2', 'typing', "matplotlib"],
    url="https://github.com/Yilmaz4/perspective.py/",
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
    download_url="https://github.com/Yilmaz4/perspective.py/archive/refs/tags/v0.3.0.tar.gz",
    keywords=["perspective-api", "api-wrapper", "python", "api"],
    long_description_content_type='text/markdown'
)