#!/usr/bin/env bash
set -euo pipefail

az vm deallocate --ids $(az vm list -g rg-empresa-x --query "[].id" -o tsv)
