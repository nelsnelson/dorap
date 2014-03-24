#!/bin/sh

PROJECT_NAME="dorap"
PROJECT_VERSION="$(cat ../src/dorap/VERSION)"

# Build the artifact
pushd ../;
python ./build.py ${PROJECT_NAME};
popd;

# Generate the debian
fpm -d python -v "${PROJECT_VERSION}" -n "${PROJECT_NAME}" -t deb --after-install ./deb/post_install.sh --after-remove ./deb/after_remove.sh -s tar "./../${PROJECT_NAME}_${PROJECT_VERSION}.tar.gz";
rm -vf "./../${PROJECT_NAME}_${PROJECT_VERSION}.tar.gz";
