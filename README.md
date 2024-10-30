[![](https://img.shields.io/badge/OS-Unix%20%7C%20MacOS-blue)](https://github.com/bioexcel/biobb)
[![](https://img.shields.io/badge/Python%20Versions-3.8%20%7C%203.9%20%7C%203.10-blue)](https://pypi.org/project/biobb/)
[![](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![](https://img.shields.io/badge/Open%20Source%3f-Yes!-blue)](https://github.com/bioexcel/biobb)

[![](https://readthedocs.org/projects/biobb/badge/?version=latest)](https://biobb.readthedocs.io/en/latest/?badge=latest)
[![](https://img.shields.io/website?down_message=Offline&label=Biobb%20Website&up_message=Online&url=https%3A%2F%2Fmmb.irbbarcelona.org%2Fbiobb%2F)](https://mmb.irbbarcelona.org/biobb/)
[![](https://img.shields.io/badge/Youtube-tutorial-blue?logo=youtube&logoColor=red)](https://www.youtube.com/watch?v=ou1DOGNs0xM)
[![](https://zenodo.org/badge/DOI/10.1038/s41597-019-0177-4.svg)](https://doi.org/10.1038/s41597-019-0177-4)
[![](https://img.shields.io/endpoint?color=brightgreen&url=https%3A%2F%2Fapi.juleskreuer.eu%2Fcitation-badge.php%3Fshield%26doi%3D10.1038%2Fs41597-019-0177-4)](https://www.nature.com/articles/s41597-019-0177-4#citeas)

[![fair-software.eu](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F-green)](https://fair-software.eu)
[![](https://www.bestpractices.dev/projects/8847/badge)](https://www.bestpractices.dev/projects/8847)
[![CITATION.cff](https://github.com/bioexcel/biobb/actions/workflows/cff-validator.yaml/badge.svg)](https://github.com/bioexcel/biobb/actions/workflows/cff-validator.yaml)

[](https://bestpractices.coreinfrastructure.org/projects/8847/badge)

[//]: # (The previous line invisible link is for compatibility with the howfairis script https://github.com/fair-software/howfairis-github-action/tree/main wich uses the old bestpractices URL)

# BioExcel Building Blocks (BioBB)

[![](https://mmb.irbbarcelona.org/biobb/assets/layouts/layout3/img/logo.png)](https://mmb.irbbarcelona.org/biobb/)

## Survey

> **Help us to improve!** 
Please help us to **improve** the **BioExcel Building Blocks** by filling in our [**2023 survey**](https://forms.gle/tAK4yGC1e7j8rRiZ8).

## Summary

The [BioExcel Building Blocks](http://mmb.irbbarcelona.org/biobb/) (BioBB) library is a collection of portable wrappers on top of common biomolecular simulation tools [Andrio, P., _et al_. BioExcel Building Blocks, a software library for interoperable biomolecular simulation workflows. _Sci Data_ **6**, 169 (2019)](https://www.nature.com/articles/s41597-019-0177-4). Created and implemented within the [BioExcel CoE](http://bioexcel.eu/), the library is designed to i) increase the interoperability between the tools wrapped; ii) ease the implementation of biomolecular simulation workflows; and iii) increase the reusability and reproducibility of the generated workflows. The library is being developed following the FAIR principles for research software development best practices. The result is a collection of building block modules, classified according to the tool being wrapped (e.g. [biobb_amber](https://github.com/bioexcel/biobb_amber) for AMBER MD package) or the functionalities offered by the tools being wrapped (e.g. [biobb_vs](https://github.com/bioexcel/biobb_vs) for Virtual Screening, [biobb_chemistry](https://github.com/bioexcel/biobb_chemistry) for chemoinformatics). Each of the module is built from a combination of software packaging ([Pip](https://pypi.org/search/?q=biobb), [BioConda](https://bioconda.github.io/search.html?q=biobb), [BioContainers](https://biocontainers.pro/registry?all_fields_search=biobb)), documentation ([ReadTheDocs](https://biobb.readthedocs.io/), [OpenAPI](https://mmb.irbbarcelona.org/biobb-api/rest), [Swagger](https://mmb.irbbarcelona.org/biobb-api/rest/swagger.json)), registry and findability ([bio.tools](https://bio.tools/biobb), [BioSchemas](https://bioschemas.org/profiles/ComputationalTool/0.5-DRAFT/), [OpenEBench](https://openebench.bsc.es/tool/biobb), [WorkflowHub](https://workflowhub.eu/programmes/2)), source code ([GitHub](https://github.com/bioexcel/biobb)) and WfMS integration -adapters- ([CWL](https://github.com/bioexcel/biobb_adapters/tree/master/biobb_adapters/cwl), [Galaxy](https://toolshed.g2.bx.psu.edu/repository?repository_id=e23296b413014cfc), [PyCOMPSs](https://github.com/bioexcel/biobb_adapters/tree/master/biobb_adapters/pycompss), [Jupyter Notebook](http://mmb.irbbarcelona.org/biobb/workflows)). 

A collection of [demonstration workflows](http://mmb.irbbarcelona.org/biobb/workflows) have been developed to showcase the library possibilities. Built using the Jupyter Noteboook GUI, the demonstration workflows offer a graphical and interactive interface, including documentation (integrated markdown) related to the workflow and the building blocks used, and also information about the pipeline and the biomolecular simulation methods used. The set of demonstration workflows are available separately on the [BioExcel GitHub](https://github.com/orgs/bioexcel/repositories?q=biobb_wf&type=all&language=&sort=) repository, with step-by-step instructions on how to reproduce them in a local machine using the Conda packaging software. There is also a [global repository for all the BioExcel Building Blocks Workflows](https://github.com/bioexcel/biobb_workflows). In this repository, there are all the versions for each workflow manager: Common Workflow Language (CWL), Galaxy, Jupyter Notebooks and Pure Python.

All the information regarding the BioExcel Building Blocks library can be found in the central [BioBB web page](http://mmb.irbbarcelona.org/biobb/). Links to source code, documentation, packages, containers, tutorials, and information from training events (e.g. BioExcel Summer/Winter School) can be found in the different web sections. 

Feedback and contact: <http://mmb.irbbarcelona.org/biobb/contact> 

## Documentation

The latest documentation of our BioBB collections can be found in our readthedocs sites:
- [biobb_amber](https://biobb-amber.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_amber): Biobb_amber is a BioBB category for AMBER MD package, allowing setup and simulation of atomistic MD simulations using AMBER MD package and its associated AMBER tools.
- [biobb_analysis](http://biobb_analysis.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_analysis): Biobb_analysis is the Biobb module collection to perform analysis of molecular dynamics simulations.
- [biobb_chemistry](http://biobb_chemistry.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_chemistry): Biobb_chemistry is the Biobb module collection to perform chemistry over molecular dynamics simulations.
- [biobb_cmip](https://biobb-cmip.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_cmip): Biobb_cmip is the Biobb module collection to compute classical molecular interaction potentials.
- [biobb_common](http://biobb_common.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_common): Biobb_common is the base package required to use the biobb packages.
- [biobb_cp2k](https://biobb-cp2k.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_cp2k): Biobb_cp2k is the Biobb module collection to compute classical molecular interaction potentials. 
- [biobb_dna](https://biobb-dna.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_dna): Biobb_dna is the Biobb module collection to perform analyses and transformations on nucleic acid trajectories and helical parameter data.
- [biobb_flexdyn](https://biobb-flexdyn.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_flexdyn): Biobb_flexdyn is the Biobb module collection for studies on the conformational landscape of native proteins.
- [biobb_flexserv](https://biobb-flexserv.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_flexserv): Biobb_flexserv is a BioBB category for biomolecular flexibility studies on protein 3D structures.
- [biobb_godmd](https://biobb-godmd.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_godmd): Biobb_godmd is the Biobb module collection to compute protein conformational transitions with the GOdMD method.
- [biobb_gromacs](https://biobb-gromacs.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_gromacs): Biobb_gromacs is the Biobb module collection to perform molecular dynamics simulations using the GROMACS MD suite.
- [biobb_io](http://biobb_io.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_io): Biobb_io is the Biobb module collection to fetch data to be consumed by the rest of the Biobb building blocks.
- [biobb_md](http://biobb_md.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_md): Biobb_md is the Biobb module collection to perform molecular dynamics simulations. **IMPORTANT:** This package has been discontinued, superseeded by [biobb_gromacs](https://github.com/bioexcel/biobb_gromacs).
- [biobb_ml](https://biobb-ml.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_ml): Biobb_ml is the Biobb module collection to perform machine learning predictions. 
- [biobb_model](http://biobb_model.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_model): Biobb_model is the Biobb module collection to check and model 3d structures, create mutations or reconstruct missing atoms.
- [biobb_pmx](http://biobb_pmx.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_pmx): Biobb_pmx is the Biobb module collection to perform [PMX](http://pmx.mpibpc.mpg.de) executions.
- [biobb_structure_utils](http://biobb_structure_utils.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_structure_utils): Biobb_structure_utils is the Biobb module collection to modify or extract information from a PDB structure file.
- [biobb_pytorch](https://biobb-pytorch.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_pytorch): Biobb_pytorch is the Biobb module collection to create and train ML & DL models using the popular PyTorch Python library.
- [biobb_vs](https://biobb-vs.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_vs): Biobb_vs is the Biobb module collection to perform virtual screening studies.
- [biobb_adapters](http://biobb_adapters.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_adapters): Biobb_adapters is the Biobb module collection to use the building blocks with several workflow managers.
- [biobb_template](http://biobb_template.readthedocs.io/en/latest/) [\[GitHub\]](https://github.com/bioexcel/biobb_template): Boilerplate code and template examples to create your own Biobbs.

More information of the BioBB collections available at the official website: [https://mmb.irbbarcelona.org/biobb/documentation/source](https://mmb.irbbarcelona.org/biobb/documentation/source)

## Videos

- BioExcel Building Blocks in BioExcel YouTube channel: [https://www.youtube.com/@BioExcelCoE/search?query=biobb](https://www.youtube.com/@BioExcelCoE/search?query=biobb)

## Workflows

- All the workflows are available at the official website: [https://mmb.irbbarcelona.org/biobb/workflows](https://mmb.irbbarcelona.org/biobb/workflows)

## Version

v5.0.0 2024.2

## Copyright & Licensing

This software has been developed in the [MMB group](http://mmb.irbbarcelona.org) at the [BSC](http://www.bsc.es/) & [IRB](https://www.irbbarcelona.org/) for the [European BioExcel](http://bioexcel.eu/), funded by the European Commission (EU H2020 [823830](http://cordis.europa.eu/projects/823830), EU H2020 [675728](http://cordis.europa.eu/projects/675728)).

* (c) 2015-2024 [Barcelona Supercomputing Center](https://www.bsc.es/)
* (c) 2015-2024 [Institute for Research in Biomedicine](https://www.irbbarcelona.org/)

Licensed under the
[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0), see the file LICENSE for details.

![](https://bioexcel.eu/wp-content/uploads/2019/04/Bioexcell_logo_1080px_transp.png "Bioexcel")
