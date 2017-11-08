from setuptools import setup,find_packages
import os,sys,errno
def readme():
    with open('README.rst') as f:
        return f.read()
def recursiveSearch(directory):
    return [os.path.join(root, name)
                 for root, dirs, files in os.walk(directory)
                 for name in files
                 if name.endswith(".DS_Store")==False]
setup(
    name='PyDMTQ',
    version='0.0.2',
    packages=find_packages(),
    url = "https://github.com/Naville/DMTQResearch",
    license='GPL',
    author='Naville',
    author_email='admin@mayuyu.io',
    description='Python Interface For DMTQ API',
    long_description=readme(),
    install_requires=['pkcs7','PyCrypto',"requests"],
    zip_safe = False,
    include_package_data=True
)
