# Submodules

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
git submodule update --init --recursive
```