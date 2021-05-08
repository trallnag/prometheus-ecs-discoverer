#!/usr/bin/env bash

project_name="prometheus_ecs_discoverer"


# ==============================================================================
# Misc


function _docs {
    echo "Create docs"

    tmp_dir=/tmp/docs
    rm -rf /tmp/docs
    mkdir -p /tmp/docs
    rm -rf docs/*
    mkdir -p docs
    poetry run pdoc --output-dir /tmp/docs --html ${project_name}
    mv /tmp/docs/${project_name}/* docs/
    rm -rf /tmp/docs
}

function _lint {
    echo "Lint project"

    poetry run flake8 --config .flake8 --statistics
}

function _requirements {
    echo "Create requirements file"

    rm -rf "requirements.txt"
    poetry export \
        --format "requirements.txt" \
        --output "requirements.txt" \
        --without-hashes
}


# ==============================================================================
# Format


function _format_style {
    echo "Format style"

    poetry run black .    
}

function _format_imports {
    echo "Format imports"

    poetry run isort --profile black .
}

function _format {
    _format_style
    _format_imports
}


# ==============================================================================
# Test


function _test {
    poetry run pytest --cov=./ --cov-report=xml
}


# ==============================================================================


function _help {
    cat << EOF
Functions you can use like this 'bash run.sh <function name>':
    help | -help | --help
    docs
    lint
    requirements
    format-style
    format-imports
    format
    test
EOF
}

if [[ $# -eq 0 ]]
then
    _help
fi

for arg in "$@"
do
    if  [ $arg = "help" ] || [ $arg = "-help" ] || [ $arg = "--help" ]; then _help
    elif [ $arg = "docs" ]; then _docs
    elif [ $arg = "lint" ]; then _lint
    elif [ $arg = "requirements" ]; then _requirements
    elif [ $arg = "format-style" ]; then _format_style
    elif [ $arg = "format-imports" ]; then _format_imports
    elif [ $arg = "format" ]; then _format
    elif [ $arg = "test" ]; then _test
    else _help
    fi
done


# ==============================================================================
