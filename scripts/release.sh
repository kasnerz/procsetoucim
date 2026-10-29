#!/bin/sh
# Make the version in progress public: copy the build that https://procsetoucim.internal.quxt.eu shows (written by
# scripts/deploy.sh) to https://procsetoucim.cz, exactly as it is, without rebuilding (user 2026-10-25).
set -eu
STACK=/opt/stacks/procsetoucim
[ -f "$STACK/site-staging/index.html" ] || { echo "no staging build; run scripts/deploy.sh first" >&2; exit 1; }
rsync -a --delete "$STACK/site-staging/" "$STACK/site/"
echo "released: https://procsetoucim.cz/"
