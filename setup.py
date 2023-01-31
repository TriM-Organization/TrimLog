# encoding:utf-8
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="TrimLog",
    version="0.6.0",
    author="FedDragon1, Eilles Wan, bgArray",
    author_email="TriM-Organization@hotmail.com",
    description="TriMO组织的python项目log和项目管理框架库。\n"
                " The Python project log and project management framework library for TriM Organization.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TriM-Organization/TrimLog",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

    ],
)
