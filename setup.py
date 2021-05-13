from setuptools import setup

with open("README.md","r") as readme_file:
    long_description = readme_file.read()

exec(open("rnmd/__init__.py").read())

setup(
    name='rnmd',
    version=__version__,
    packages=['rnmd'],
    include_package_data=True,
    python_requires='>=3',
    entry_points={
        'console_scripts':['rnmd = rnmd.rnmd:main']
    },
    description='A runtime for executing interpreted code of markdown files and making them available from anywhere',
    long_description=long_description,
    long_description_content="text/markdown",
    author="Markus Peitl",
    author_email='office@markuspeitl.com',
    url='https://github.com/MarkusPeitl/rnmd',
    classifiers=[
        "Programming Language :: Python :: 3"
        "License :: ",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 (LGPLv2)",
        "Natural Language :: English",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Documentation",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
)