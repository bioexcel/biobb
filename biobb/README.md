# Submodules
First fetch all the submodules tags:
```bash
git submodule foreach --recursive 'git fetch --tags'
```

To update the submodules to a specific tag, you can use the following command:
```bash
git submodule foreach --recursive 'git checkout YOUR_TAG_NAME || true'
```

To update the submodules to the last tagged version:
```bash
git submodule foreach --recursive 'git checkout $(git tag --sort=-v:refname | head -n 1)'
```

To pull while cloning the repository:
```bash
git clone --recurse-submodules https://github.com/bioexcel/biobb.git
```

To pull after cloning:
```bash
git submodule update --remote --merge --recursive
```

# Conda Environment Setup for BioBB
Make the environment with all the BioBB packages and dependencies:
```bash
mamba env create -f biobb/biobb_all.yml
```

Make conda-pack:
```bash
conda activate biobb_all
conda-pack -o biobb_all.tar.gz
```