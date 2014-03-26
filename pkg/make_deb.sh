#!/bin/sh

PROJECT_NAME="dorap"
PROJECT_VERSION="$(cat ./src/dorap/VERSION)"

# Build the artifact
chuckbox pack ${PROJECT_NAME};

# Generate the debian
fpm -d python -v "${PROJECT_VERSION}" -n "${PROJECT_NAME}" -t deb --after-install ./pkg/deb/post_install.sh --after-remove ./pkg/deb/after_remove.sh -s tar "./${PROJECT_NAME}_${PROJECT_VERSION}.tar.gz";
rm -vf "./${PROJECT_NAME}_${PROJECT_VERSION}.tar.gz";
