#!/usr/bin/env bash

set -euxo pipefail

# This script obtains a specific version of an OpenShift sub-product documentation
# and generates markdown versions of the contents. The settings below are
# configured to obtain Red Hat OpenShift Service on AWS (ROSA) documentation for
# version 4.12, and generate GitHub-flavored Markdown from them.

# The documentation is obtained directly from the OpenShift documentation
# repository: https://github.com/openshift/openshift-docs.git

# The script uses that repository's own build scripts to generate DocBook files
# for the selected product/version. It then uses pandoc to convert these DocBook
# files into the final format.

# Settings
distro="openshift-rosa"
product="Red Hat OpenShift Service on AWS"
version="4.12"
# Output format (used for pandoc's target selection)
format="gfm"  # gfm == GitHub-flavored Markdown
ext="md"  # file extension for the generated files
# Where to place the generated files
SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
destdir=$(realpath "${SCRIPT_DIR}/../data/raw")

# ---- Script begins ----
# Setting things up
mkdir -p ${destdir}
workdir=$(mktemp -d)
function finish {
    rm -rf ${workdir}
}
trap finish EXIT

# Get a shallow copy of the relevant openshift docs branch
cd ${workdir}
git clone --depth=1  https://github.com/openshift/openshift-docs.git --branch "enterprise-${version}"
cd openshift-docs

# Build the DocBook files using the utilities in openshift-docs
python build.py --distro="${distro}" --product="${product}" --version=${version:0:1} --no-upstream-fetch
python makeBuild.py

# Convert DocBook files to the desired format
docsdir="drupal-build"  # this is where build.py places docbook files
files=$(find ${docsdir} -name master.xml)  # all files are named master.xml
for file in $files; do
    chapter=${file#${docsdir}/${distro}/}  # strip distro-based path
    chapter=${chapter%/build*}             # strip trailing build path
    outfile="${destdir}/${chapter}.${ext}"
    echo "Processing ${chapter}"
    pandoc -f docbook -t ${format} --columns=666 -o ${outfile} ${file}
    # Remove <div> tags
    sed -i -e 's#</*div[^>]*>##' ${outfile}
done
