#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    with open('README.rst', 'r') as f:
        return f.read()
setup(
    name='sendgrid_parse',
    version='0.2',
    description="Access SendGrid's Inbound Parse emails into a dictionary",
    long_description=readme(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Communications :: Email',
    ],
    keywords="sendgrid inbound parse email flask django",
    url='https://github.com/coolharsh55/sendgrid_parse',
    author='coolharsh55',
    author_email="me@harshp.com",
    license='MIT',
    packages=['sendgrid_parse'],
    zip_safe=False,
)
