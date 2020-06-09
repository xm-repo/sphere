#!/bin/bash

sudo apt-get -y install unzip build-essential zlib1g-dev

HOME_DIR="$(pwd)"
SOURCES_DIR="$(pwd)/sources"
EXE_DIR="$(pwd)/executables"

rm -r "$SOURCES_DIR"
rm -r "$EXE_DIR"

mkdir -p executables
mkdir -p sources && cd sources

cd "$SOURCES_DIR"
echo "MiniSAT 2.2"
mkdir -p MiniSAT && cd MiniSAT
git clone https://github.com/MontyThibault/minisat
export MROOT="../"
cd "minisat/" && make
cp "build/release/bin/minisat" "$EXE_DIR/minisat_2.2"

cd "$SOURCES_DIR"
echo "Glucose 4.1"
mkdir -p Glucose && cd Glucose
wget "https://www.labri.fr/perso/lsimon/downloads/softwares/glucose-syrup-4.1.tgz"
tar --extract --file "glucose-syrup-4.1.tgz"
export MROOT="../"
cd "glucose-syrup-4.1/simp" && make && cp "glucose" "$EXE_DIR/glucose_4.1_simp"
cd "../parallel" && make && cp "glucose-syrup" "$EXE_DIR/glucose_4.1_parallel(glucose-syrup)"

cd "$SOURCES_DIR"
echo "lingeling"
mkdir -p lingeling && cd lingeling
git clone "https://github.com/arminbiere/lingeling"
export MROOT="../"
cd lingeling && ./configure.sh && make
cp "lingeling" "$EXE_DIR/lingeling"
cp "plingeling" "$EXE_DIR/plingeling"
cp "treengeling" "$EXE_DIR/treengeling"
cp "ilingeling" "$EXE_DIR/ilingeling"

cd "$SOURCES_DIR"
echo "zChaff 2004.11.15"
mkdir -p zChaff && cd zChaff
wget "https://www.princeton.edu/~chaff/zchaff/zchaff.2004.11.15.zip"
unzip "zchaff.2004.11.15.zip"
cd "zChaff" 
sed -i '1i#include <cstring>' sat_solver.cpp
export MROOT="../"
make && cp "zchaff" "$EXE_DIR/zchaff.2004.11.15"

cd "$SOURCES_DIR"
echo "MapleSAT"
mkdir -p MapleSAT && cd MapleSAT
wget "https://sites.google.com/a/gsd.uwaterloo.ca/maplesat/MapleSAT.zip" && unzip MapleSAT 
export MROOT="../"
cd simp && make CMD_CFLAGS=-fpermissive && cp "maplesat" "$EXE_DIR/maplesat"

cd "$SOURCES_DIR"
echo "MapleCOMSPS_pure_LRB"
mkdir -p MapleCOMSPS_pure_LRB && cd MapleCOMSPS_pure_LRB
wget "https://sites.google.com/a/gsd.uwaterloo.ca/maplesat/MapleCOMSPS_pure_LRB.zip" && unzip MapleCOMSPS_pure_LRB && cd MapleCOMSPS_pure_LRB
export MROOT="../"
cd simp
sed -i '22s/.*/CFLAGS    ?= -Wall -Wno-parentheses -fpermissive/' ../mtl/template.mk
make && cp "minisat" "$EXE_DIR/MapleCOMSPS_pure_LRB"

cd "$SOURCES_DIR"
echo "MapleCOMSPS_pure_CHB"
mkdir -p MapleCOMSPS_pure_CHB && cd MapleCOMSPS_pure_CHB
wget "https://sites.google.com/a/gsd.uwaterloo.ca/maplesat/MapleCOMSPS_pure_CHB.zip" && unzip MapleCOMSPS_pure_CHB && cd MapleCOMSPS_pure_CHB
export MROOT="../"
cd simp
sed -i '22s/.*/CFLAGS    ?= -Wall -Wno-parentheses -fpermissive/' ../mtl/template.mk
make && cp "minisat" "$EXE_DIR/MapleCOMSPS_pure_CHB"

cd "$SOURCES_DIR"
echo "MapleCOMSPS_CHB"
mkdir -p MapleCOMSPS_CHB && cd MapleCOMSPS_CHB
wget "https://sites.google.com/a/gsd.uwaterloo.ca/maplesat/MapleCOMSPS_CHB.zip" && unzip MapleCOMSPS_CHB && cd MapleCOMSPS_CHB
export MROOT="../"
cd simp
sed -i '22s/.*/CFLAGS    ?= -Wall -Wno-parentheses -fpermissive/' ../mtl/template.mk
make && cp "minisat" "$EXE_DIR/MapleCOMSPS_CHB"

cd "$SOURCES_DIR"
echo "MapleCOMSPS_LRB"
mkdir -p MapleCOMSPS_LRB && cd MapleCOMSPS_LRB
wget "https://sites.google.com/a/gsd.uwaterloo.ca/maplesat/MapleCOMSPS_LRB.zip" && unzip MapleCOMSPS_LRB && cd MapleCOMSPS_LRB
export MROOT="../"
cd simp
sed -i '22s/.*/CFLAGS    ?= -Wall -Wno-parentheses -fpermissive/' ../mtl/template.mk
make && cp "minisat" "$EXE_DIR/MapleCOMSPS_LRB"

cd "$SOURCES_DIR"
echo "cadical"
mkdir -p cadical && cd cadical
git clone https://github.com/arminbiere/cadical && cd cadical
./configure && make && 
cp "build/cadical" "$EXE_DIR/cadical"

cd "$SOURCES_DIR"
echo "picosat"
mkdir -p picosat && cd picosat
wget "http://fmv.jku.at/picosat/picosat-965.tar.gz" && tar --extract --file "picosat-965.tar.gz"
cd picosat-965 && ./configure.sh && make && cp "picosat" "$EXE_DIR/picosat"

cd "$SOURCES_DIR"
echo "kissat"
mkdir -p kissat && cd kissat
git clone "https://github.com/arminbiere/kissat" && cd kissat && ./configure && make && cp "build/kissat" "$EXE_DIR/kissat"

cd "$SOURCES_DIR"
echo "CryptoMiniSat"
git clone "https://github.com/msoos/cryptominisat"
cd cryptominisat
sudo apt-get -y cmake install zlib1g-dev libboost-program-options-dev libm4ri-dev libsqlite3-dev help2man
mkdir build && cd build && cmake .. && make && cp "cryptominisat5" "$EXE_DIR/cryptominisat5" 

cd "$SOURCES_DIR"
echo "rsat"
mkdir -p rsat && cd rsat
wget "http://www3.cs.stonybrook.edu/~algorith/implement/rsat/distrib/rsat_2.01_linux.tar.gz" && tar --extract --file "rsat_2.01_linux.tar.gz"
cp "rsat_2.01_linux/rsat" "$EXE_DIR/rsat"
cp "rsat_2.01_linux/SatElite" "$EXE_DIR/SatElite"

: '
cd "$SOURCES_DIR"
echo "CryptoMiniSat"
git clone "https://github.com/msoos/cryptominisat"
cd cryptominisat
sudo apt-get -y cmake install zlib1g-dev libboost-program-options-dev libm4ri-dev libsqlite3-dev help2man
mkdir build && cd build && cmake .. && make

cd "$SOURCES_DIR"
echo "RISS"
mkdir -p RISS && cd RISS
git clone https://github.com/nmanthey/riss-solver
export CFLAGS=-fpermissive
export CXXFLAGS=-fpermissive
cd riss-solver && mkdir build && cd build && cmake .. && make
'
