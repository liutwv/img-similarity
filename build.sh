#!/bin/bash
# ----------------------------------------------------------------------------
# [Author] LiuTao
#
#  This script is used to deploy the Python Application to company's Docker Hub.
#
# ----------------------------------------------------------------------------

# Get application version from version.properties
version=$(cat version.properties | grep "version=[0-9\.]" | cut -d "=" -f 2)
tmp=${version#*\"}
version=${tmp%\"*}

# Automatically increment application version
# For example: 0.1 -> 0.2
increment_version ()
{
  declare -a part=( ${1//\./ } )
  declare    new
  declare -i carry=1

  for (( CNTR=${#part[@]}-1; CNTR>=0; CNTR-=1 )); do
    len=${#part[CNTR]}
    new=$((part[CNTR]+carry))
    [ ${#new} -gt $len ] && carry=1 || carry=0
    [ $CNTR -gt 0 ] && part[CNTR]=${new: -len} || part[CNTR]=${new}
  done
  new="${part[*]}"
  version="${new// /.}"
}

increment_version $version
sed -i -e "s/version=.*/version=$version/g" version.properties

docker build -t img-similarity:$version .
docker tag img-similarity:$version xxx/img-similarity:$version
docker push xxx/img-similarity:$version