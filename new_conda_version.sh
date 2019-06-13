#!/usr/bin/env bash

#Usage: ./new_conda_version.sh
#Activate conda
read -p "Repository name ie biobb_md : " REPOSITORY
read -p "Version number ie 0.1.2 : " version
read -p "Commint message ie Feb 2019 Release : " message
echo "Repository: $REPOSITORY"
echo "Version: $version"
echo "Message: $message"
atom /Users/pau/projects/$REPOSITORY/setup.py
read -p "Modify setup.py with the new version number and press any key..." -n1 -s
echo ""
read -p "Modify README.md with the new version number and press any key..." -n1 -s
echo ""
cd /Users/pau/projects/$REPOSITORY
cp -v /Users/pau/projects/$REPOSITORY/README.md /Users/pau/projects/$REPOSITORY/$REPOSITORY/docs/source/readme.md
git status ; git add . ; git commit -m "$message" ; git push ; git push bioexcel
git tag -a v$version -m "$message"; git push origin v$version; git push bioexcel v$version
python3 setup.py sdist bdist_wheel; python3 -m twine upload dist/* <<< andriopau
rm -rfv $REPOSITORY.egg-info dist build

#Bioconda
rm -rf /Users/pau/$REPOSITORY 2> /dev/null
retval=1
while [ $retval -ne 0 ]
do
  echo "Sleeping for 5 seconds..."
  sleep 5
  cd /Users/pau; conda skeleton pypi $REPOSITORY --version $version
  retval=$?
done
atom /Users/pau/$REPOSITORY/meta.yaml
read -p "Copy the headers (lines that starts with {%) from  ~/$REPOSITORY/meta.yaml and press any key..." -n1 -s
echo ""
cd /Users/pau/other_projects/bioconda-recipes/
git checkout -f master; git pull origin master
git branch -D $REPOSITORY; git push origin --delete $REPOSITORY; git checkout -b $REPOSITORY
atom /Users/pau/other_projects/bioconda-recipes/recipes/$REPOSITORY
read -p "Modify recipes/$REPOSITORY/build.sh and press any key..." -n1 -s
echo ""
read -p "Modify recipes/$REPOSITORY/meta.yaml paste the headers from ~/$REPOSITORY/meta.yaml and press any key..." -n1 -s
echo ""
git status; git add recipes/$REPOSITORY/*
git commit -m "$message"
git push -u origin $REPOSITORY
open https://github.com/bioconda/bioconda-recipes/pull/new/$REPOSITORY
