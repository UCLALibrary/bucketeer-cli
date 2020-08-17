# Bucketeer CLI &nbsp;[![Build Status](https://travis-ci.com/UCLALibrary/bucketeer-cli.svg?branch=main)](https://travis-ci.com/UCLALibrary/bucketeer-cli)

Uploads CSV files to the [Bucketeer](https://github.com/UCLALibrary/bucketeer) service for processing.

## Installation

First, ensure that you have Bash, cURL, Python 3.6+ and Pip installed on your system.

When that's done, clone the repository and follow the development instructions below (install script coming soon).

## Usage

After it's installed, you can see the available options by running:

    bucketeer_cli --help

Note that access to UCLA's Bucketeer service is limited to campus IP addresses, so off-campus users must [connect to the VPN](https://www.it.ucla.edu/it-support-center/services/virtual-private-network-vpn-clients).

The SRC argument supports standard [filename globbing](https://en.wikipedia.org/wiki/Glob_(programming)) rules. In other words, `*.csv` is a valid entry for the SRC argument.

*There are limits* to how many arguments can be sent to a command. This depends on your OS and its configuration. See this [StackExchange](https://unix.stackexchange.com/questions/110282/cp-max-source-files-number-arguments-for-copy-utility) post for more information.

Bucketeer CLI will ignore any files that do not end with `.csv`, so a command of `bucketeer_cli *.*` should be safe to run. Bucketeer CLI does not recursively search folders.

Bucketeer CLI creates a single log file in the working directory. There is no limit on how large this file can become, so the user is responsible for modifying or deleting it if it becomes too large.

## Development

It is recommended that developers create a virtual environment for local Python development. After cloning the repository, here's a quick way to get setup:

    #!/bin/bash

    python3 -m venv venv_bucketeer_cli
    . venv_bucketeer_cli/bin/activate
    pip install -e . black pytest

To run the tests:

    pytest

Before pushing, make sure you format all the Python source files:

    black *.py

You can use the included pre-push script as a Git hook to run these checks automatically on `git push`:

    mv -i pre-push .git/hooks/

## Releases

To create a new release:

1. Update the version number in `setup.py`.
1. Push a new Git tag using the new version number:
    ```
    #!/bin/bash

    NEW_VERSION=0.1.0
    git tag -s $NEW_VERSION -m "Tagging \"$NEW_VERSION\" for release"
    git push origin $NEW_VERSION
    ```
1. Create a new release using the GitHub UI.

## Contact

Feel free to use this project's [issues queue](https://github.com/uclalibrary/bucketeer-cli/issues) to ask questions, make suggestions, or provide other feedback.
