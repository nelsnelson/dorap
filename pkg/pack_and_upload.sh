#!/bin/bash

if [ ! -d /tmp/dorap_venv ]; then
    virtualenv /tmp/dorap_venv;
fi

export PATH=/tmp/dorap_venv/bin:$PATH;

# Install things we might need
pip install --upgrade chuckbox cython;

# Get our version and package name
VERSION="$(cat src/dorap/VERSION)";
PKG_NAME="dorap_${VERSION}_amd64.deb";

# Build the package
bash ./pkg/make_deb.sh;

# Upload the package
rps_client.sh upload_new ${PKG_NAME};
rps_client.sh promote staging ${PKG_NAME};

# Remove the local copy of the package
rm -vf ${PKG_NAME};
