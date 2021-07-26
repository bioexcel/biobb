import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb",
    version="3.6.0",
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
                      'biobb_common==3.6.0',
                      'biobb_io==3.6.0',
                      'biobb_model==3.6.0',
                      'biobb_md==3.6.0',
                      'biobb_analysis==3.6.0',
                      'biobb_chemistry==3.6.0',
                      'biobb_pmx==3.6.0',
                      'biobb_structure_utils==3.6.1',
                      'biobb_ml==3.6.0',
                      'biobb_amber==3.6.0',
                      'biobb_vs==3.6.0'
                      ],
    python_requires='==3.7.*',
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
