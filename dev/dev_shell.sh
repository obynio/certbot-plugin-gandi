#!/bin/bash
set -e

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
PROJ_DIR="$(dirname "$SCRIPT_DIR")"

docker run -it --rm --entrypoint /bin/sh -e GANDI_API_KEY -v "$PROJ_DIR:/tmp/work" certbot/certbot:v0.22.0 '/tmp/work/dev/tools/initfile.sh'
