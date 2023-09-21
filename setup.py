import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="biobb",
    version="4.1.0",
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
    install_requires=['biobb_amber==4.1.0',
                      'biobb_analysis==4.1.0',
                      'biobb_chemistry==4.1.0',
                      'biobb_cmip==4.1.0',
                      'biobb_common==4.1.0',
                      'biobb_cp2k==4.1.0',
                      'biobb_dna==4.1.0',
                      'biobb_flexdyn==4.1.0',
                      'biobb_flexserv==4.1.0',
                      'biobb_godmd==4.1.0',
                      'biobb_gromacs==4.1.0',
                      'biobb_io==4.1.0',
                      # 'biobb_md==3.7.2',
                      'biobb_ml==4.1.0',                
                      'biobb_model==4.1.0',
                      'biobb_pmx==4.1.0',
                      'biobb_structure_utils==4.1.0',
                      'biobb_vs==4.1.1'
                      ],
    python_requires='>=3.8',
    classifiers=(
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
    ),
)
