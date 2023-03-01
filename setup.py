from setuptools import setup, find_packages
import re

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("murph/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name='murph',
    version=version,
    license='BSD 3-Clause "New" or "Revised"',
    author="Alexandru Plesoiu",
    author_email='alexandru@mgesoftware.com',
    description="Murph is a fast and efficient Python framework for building GRPC services. With automatic Protobuf file generation and a simplified development process, Murph makes it easy to build high-performance services with ease.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["examples*"]),
    url='https://github.com/mgesoftware/murph',
    keywords='grpc, grpc-services, grpc-framework, python-framework, protobufs, django-like-models, async, high-performance, efficient, network-programming, web-development, real-time-applications, mge, mgesoftware, murph, murph-framework, framework, django, flask, grpcio',
    install_requires=requirements,
    python_requires='>=3.8',
    project_urls={
        "Documentation": "https://murph.readthedocs.io",
        "Source Code": "https://github.com/mgesoftware/murph",
        "Issue Tracker": "https://github.com/mgesoftware/murph/issues",
        "PyPI": "https://pypi.org/project/murph/",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: System :: Networking",
        "Topic :: Internet",
        "License :: OSI Approved :: BSD License",
        "Framework :: AsyncIO",
        "Framework :: Django",
        "Framework :: Flask",
        "Typing :: Typed"
    ]
)
