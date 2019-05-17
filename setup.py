import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb",
    version="1.0.1",
    author="Biobb developers",
    author_email="pau.andrio@bsc.es",
    description="Biobb module collection.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Bioinformatics Workflows BioExcel Compatibility",
    url="https://github.com/bioexcel/biobb",
    project_urls={
        "Documentation": "http://biobb.readthedocs.io/en/latest/",
        "Bioexcel": "https://bioexcel.eu/"
    },
    packages=setuptools.find_packages(exclude=['docs', 'test']),
    install_requires=['m2r',
                      'biobb_common==1.1.6',
                      'biobb_io==1.1.6',
                      'biobb_model==1.1.9',
                      'biobb_md==1.1.6',
                      'biobb_analysis==1.0.3',
                      'biobb_chemistry==1.0.6',
                      'biobb_pmx==1.0.0'
                      ],
    python_requires='==3.6.*',
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
