from setuptools import setup, find_packages

setup(
    name='gserp_api',
    version='0.1.5',
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4==4.12.3',
        'boto3==1.35.76',
        'requests==2.32.3',
        'requests-ip-rotator==1.0.14',

    ],
    author='Rushabh Agarwal',
    author_email='rushabh.agarwal9@gmail.com',
    description='Open Source Google SERP API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rushout09/gserp-api',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)