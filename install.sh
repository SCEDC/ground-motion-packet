#!/bin/bash

unamestr=`uname`
env_file=environment.yml
if [ "$unamestr" == 'Linux' ]; then
    prof=~/.bashrc
    mini_conda_url=https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    matplotlibdir=~/.config/matplotlib
elif [ "$unamestr" == 'FreeBSD' ] || [ "$unamestr" == 'Darwin' ]; then
    prof=~/.bash_profile
    mini_conda_url=https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
    matplotlibdir=~/.matplotlib
else
    echo "Unsupported environment. Exiting."
    exit
fi

source $prof

echo "Path:"
echo $PATH

VENV=gmpacket_env
PYVER=3.9

# Is conda installed?
conda --version
if [ $? -ne 0 ]; then
    echo "No conda detected, installing miniconda from ${mini_conda_url}..."

    curl -L $mini_conda_url -o miniconda.sh;
    if [ $? -ne 0 ]; then
        echo "Failed to download ${mini_conda_url}, exiting."
        exit 1
    fi
    echo "Install directory: $HOME/miniconda"

    if [ -e miniconda.sh ]; then
        echo "Found shell script."
    else
        echo "Failed to download ${mini_conda_url}, exiting."
        exit 1
    fi

    # Is the shell script really a shell script?
    echo "This should say 'shell script', or something similar..."
    file miniconda.sh

    # Is the shell script of non-zero size?
    echo "This file size should be non-zero..."
    ls -lh miniconda.sh

    echo "####Running miniconda shell script..."
    bash miniconda.sh -f -b -p $HOME/miniconda
    echo "###Done running miniconda shell script..."

    # Need this to get conda into path
    . $HOME/miniconda/etc/profile.d/conda.sh
else
    echo "conda detected, installing $VENV environment..."
fi

echo "PATH:"
echo $PATH
echo ""


# Choose an environment file based on platform
echo ". $HOME/miniconda/etc/profile.d/conda.sh" >> $prof

# Start in conda base environment
echo "Activate base virtual environment"
conda activate base

# Remove existing environment if it exists
conda remove -y -n $VENV --all

# Create a conda virtual environment
echo "Creating the $VENV virtual environment:"
mamba create -y -n $VENV python=$PYVER pip

# Bail out at this point if the conda create command fails.
# Clean up zip files we've downloaded
if [ $? -ne 0 ]; then
    echo "Failed to create conda environment.  Resolve any conflicts, then try again."
    exit
fi


# Activate the new environment
echo "Activating the $VENV virtual environment"
conda activate $VENV

# This package
echo "Installing $VENV..."
pip install -e .[dev,test]

# Tell the user they have to activate this environment
echo "Type 'conda activate $VENV' to use this new virtual environment."
