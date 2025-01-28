https://www.sternwarte.uni-erlangen.de/sixte/linux/
SIXTE is a software used to simulate X-ray telescope observation simulations. Made at Remeis Observatory.

# Installation
To install, follow these steps:
## 0. Install Heasoft:
current version of NASA’s HEASOFT package: https://heasarc.gsfc.nasa.gov/lheasoft/
## 1. Get the dependencies:
These are the ubuntu-linux package names, other Linux distributions will use similar package names
	1. gcc, g++, gfortran
	2. libreadline-dev
	3. libncurses-dev
	4. libexpat1-dev
	5. libgsl0-dev
	6. libboost-dev
	7. libcmocka-dev

```sh
sudo apt-get install gcc g++ gfortran libreadline-dev libncurses-dev libexpat1-dev libgsl0-dev libboost-dev libcmocka-dev
```
## 2. Download the packages: 
Namely:
1. SIMPUT: [simput-2.6.3.tar.gz](https://www.sternwarte.uni-erlangen.de/~sixte/downloads/sixte/simput-2.6.3.tar.gz)
2. SIXTE: [sixte-3.0.5.tar.gz](https://www.sternwarte.uni-erlangen.de/~sixte/downloads/sixte/sixte-3.0.5.tar.gz)
And optionally the [instrument files](https://www.sternwarte.uni-erlangen.de/sixte/instruments/)

## 3. Extract into a  folder
Make a folder (say in the Desktop folder) where you want SIXTE to be installed. Inside, place the extracted folders from the two `.tar.gz` files
```sh
cd Desktop
mkdir SIXTE
mkdir SIXTE/simput SIXTE/sixte SIXTE/installation

```