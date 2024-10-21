

UV_COMMAND := $(shell command -v uv 2> /dev/null)
all:
ifndef UV_COMMAND
    $(error "uv is not available please install uv (see https://docs.astral.sh/uv/getting-started/installation/ )")
endif




