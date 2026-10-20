#!/usr/bin/env bash
set -euo pipefail

GRUPO="rg-empresa-x"
REGION="${REGION:-northcentralus}"
VNET="vnet-empresa-x"

az group create -n "$GRUPO" -l "$REGION" -o none

az network vnet create -g "$GRUPO" -n "$VNET" --address-prefixes 10.0.0.0/24 -o none

az network vnet subnet create -g "$GRUPO" --vnet-name "$VNET" -n snet-visitas --address-prefixes 10.0.0.0/26 -o none
az network vnet subnet create -g "$GRUPO" --vnet-name "$VNET" -n snet-ventas --address-prefixes 10.0.0.64/27 -o none
az network vnet subnet create -g "$GRUPO" --vnet-name "$VNET" -n snet-ti --address-prefixes 10.0.0.96/27 -o none
az network vnet subnet create -g "$GRUPO" --vnet-name "$VNET" -n snet-datacenter --address-prefixes 10.0.0.128/28 -o none

az vm create -g "$GRUPO" -n vm-ventas-1 \
  --image Ubuntu2204 --size Standard_B2ats_v2 \
  --vnet-name "$VNET" --subnet snet-ventas --private-ip-address 10.0.0.68 \
  --admin-username azureuser --ssh-key-values ~/.ssh/id_ed25519.pub -o none

az vm create -g "$GRUPO" -n vm-ventas-2 \
  --image Ubuntu2204 --size Standard_B2ats_v2 \
  --vnet-name "$VNET" --subnet snet-ventas --private-ip-address 10.0.0.69 \
  --public-ip-address "" \
  --admin-username azureuser --ssh-key-values ~/.ssh/id_ed25519.pub -o none

echo "IP pública de vm-ventas-1:"
az vm show -d -g "$GRUPO" -n vm-ventas-1 --query publicIps -o tsv
