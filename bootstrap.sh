#!/bin/bash
# :: bootstrap.sh
################################################
# Sets up the virtualenv, or
# destroys it, as needed.
################################################
# :: Created By: Benji Brandt <benjibrandt@ucla.edu>
# :: Creation Date: 9 April 2019

##############################################
# CONSTANTS
##############################################
PYTHON=python3 # needs to not be readonly for the --anaconda flag
PIP=pip3 # see above
readonly REQUIRED_PKGS=.bootstrap/requirements.txt
readonly USAGE_MSG="~~~\n\
Sets up the needed python virtualenv, or destroys it.\n\
Think of it as the thing you gotta do to do actual work.\n\
~~~\n\
Usage: ./bootstrap.sh [options]\n\
~~~\n"
readonly VALID_OPTS="Valid options:\n\
\t1) -c|--clean: blow away the virtualenv and clean/remove associated files.\n\
\t2) -a|--anaconda: run bootstrap installation with the assumption that the system python installation is anaconda's.\n\
\t3) -m|--macosmatplot: adjust specified backend for matplotlib to work with macOS via a dot-file modification.
\t4) -u|--usage: display this usage message.\n\
\n"

##############################################
# ARGUMENT PARSING
##############################################
CLEAN=false

POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
  -c|--clean)
    CLEAN=true
    shift # past argument
  ;;
  -a|--anaconda)
    if [[ $(which python | grep -F anaconda) != "" ]]; then
      echo "Accounting for anaconda python installation." 
      PYTHON=python
      PIP=pip
      printf "Note that \`which python\` yields: "
      which python
    else
      echo "ERROR: \`which python\` does not yield an anaconda-based python installation."
      printf "Note that \`which python\` yields: "
      which python
      echo "Please do not use the -a|--anaconda option if your default python is not anaconda based."
      exit 1
    fi
    shift
  ;;
  -m|--macosmatplot)
    if [[ $(cat ~/.matplotlib/matplotlibrc | grep "backend: TkAgg") == "" ]]; then
      echo "Adjusting ~/.matplotlib/matplotlibrc for macOS backend."
      echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
      echo "Adjustment successful."
    else
      echo "~/.matplotlib/matplotlibrc already adjusted for macOS backend. Ignoring -m flag."
    fi
    shift
  ;;
  -u|--usage)
    printf "$USAGE_MSG"
    printf "$VALID_OPTS"
    exit 0
  ;;
  *) # unknown option
    echo "ERROR: unknown option specified."
    printf "$VALID_OPTS"
    exit 1
  ;;
esac
done
set -- "${POSITIONAL[@]}" # restore positional parameters

##############################################
# FUNCTIONS
##############################################

# @param1: the name of the app/pkg to check for in the path
verifyPathInstallaton ()
{
  if $1 --version &> /dev/null; then
    return 0
  else
    return 1
  fi
}

buildVirtualEnv ()
{
  $PYTHON -m virtualenv build || return 1
  source build/bin/activate || return 1
  printf "Using virtualenv pip: "
  which pip
  pip install -r $REQUIRED_PKGS || return 1
  deactivate || return 1
  return 0
}

printErrorFixSuggestion ()
{
  if [[ $(which python | grep -F anaconda) != "" ]]; then
    echo "It appears your default python is anaconda-based. Try \`./bootstrap.sh --clean && ./bootstrap.sh --anaconda\`."
  else
    echo "Try \`./bootstrap.sh --clean\`, and then re-run bootstrap."
  fi
}

##############################################
# MAIN
##############################################

main ()
{
  if $CLEAN; then
    echo "Cleaning..."
    rm -rf build
    rm -rf __pycache__
    find . -name "__pycache__" -delete
    find . -name "*.pyc" -delete
    echo "Done!"
  else
    if [[ "$VIRTUAL_ENV" != "" ]]; then 
      echo "Already in a virtualenv. No need to bootstrap."
      exit 0
    fi
    if [ -f build/bin/$PYTHON ] || [ -f build/bin/pip ] ; then
      echo "virtualenv already setup. No need to bootstrap. Did you mean to clean?"
      exit 0
    fi

    echo "Verifying dependencies..."
    if verifyPathInstallaton $PIP; then
      printf "\t✓ $PIP is available in the PATH\n"
    else
      printf "\t✗ $PIP is available in the PATH\n\n"
      echo "ERROR: could not find $PIP in the PATH. Please ensure you've installed $PIP and properly set your PATH variable."
      exit 1
    fi

    if verifyPathInstallaton $PYTHON; then
      printf "\t✓ $PYTHON is available in the PATH\n"
    else
      printf "\t✗ $PYTHON is available in the PATH\n\n"
      echo "ERROR: could not find $PYTHON in the PATH. Please ensure you've installed $PYTHON and properly set your PATH variable."
      exit 1
    fi

    if [[ $($PIP list | grep -F virtualenv) != "" ]]; then
      printf "\t✓ virtualenv is installed\n\n"
    else
      printf "\t✗ virtualenv is installed\n"
      printf "ERROR: virtualenv not installed, acquiring...\n\n"
      $PYTHON -m $PIP install --user virtualenv
      rc=$?; if [[ $rc != 0 ]]; then 
        echo "ERROR: virtualenv failed to install."
        printErrorFixSuggestion
        exit $rc
      else
        printf "\n\t✓ virtualenv acquired successfully\n\n"
      fi
    fi

    echo "Building virtualenv..."
    echo "---"
    if buildVirtualEnv; then
      echo "---"
      echo "Successfully built virtualenv!"
      echo "Run \`source build/bin/activate\` from the root of the repo to engage the virtualenv."
    else
      echo "---"
      echo "ERROR: failed to build virtualenv."
      printErrorFixSuggestion
      exit 1
    fi
  fi
  exit 0
}

main
