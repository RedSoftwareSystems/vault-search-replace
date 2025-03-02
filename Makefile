UV_COMMAND := $(shell command -v uv 2> /dev/null)

.PHONY: all clean

all: setup test package
ifndef UV_COMMAND
    $(error "uv is not available please install uv (see https://docs.astral.sh/uv/getting-started/installation/ )")
endif

setup:
	@echo "Setting up the environment"


clean:
	@echo "Cleaning up..."
	rm -rf __pycache__ *.pyc


