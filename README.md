# Redes Proyecto Final

CC3067 Redes, Universidad del Valle de Guatemala, 2026.

Red en la nube para XSecurity, una startup de ciberseguridad. En la Fase 1 se dividió el bloque 10.0.0.0/24 en cuatro subredes (Visitas, Ventas, TI y Data Center), se creó la red en Azure y se probó con un ping entre dos máquinas virtuales de Ventas.

El reporte está en [fase1/reporte/Reporte_Fase1_Redes.pdf](fase1/reporte/Reporte_Fase1_Redes.pdf).

## Cómo correr el proyecto

**1. Clonar el repositorio y entrar a la carpeta**

```bash
git clone https://github.com/GenserDev/Redes-PFinal.git && cd Redes-PFinal
```

**2. Instalar Azure CLI e iniciar sesión**

```bash
brew install azure-cli && az login
```

**3. Crear la red y las máquinas virtuales**

```bash
bash fase1/azure/desplegar.sh
```

**4. Entrar a vm-ventas-1 con la IP que imprime el script y hacer ping**

```bash
ssh azureuser@IP_PUBLICA
```

```bash
ping -c 4 10.0.0.69
```

**5. Borrar todo al terminar**

```bash
bash fase1/azure/limpiar.sh
```

## Notas

**La suscripción Azure for Students solo permite cinco regiones.** El script usa `northcentralus`. Para otra región se antepone `REGION=westus`.

**El script usa la llave `~/.ssh/id_ed25519.pub`.** Si no existe, se crea con `ssh-keygen -t ed25519`.

**Los discos y la IP pública cobran aunque las VMs estén apagadas.** Por eso conviene correr `limpiar.sh` y no solo `apagar.sh`.

**El cálculo de subredes se puede repetir** con `python3 fase1/subneteo/subneteo.py`.
