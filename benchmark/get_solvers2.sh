#!/bin/bash

mkdir -p sat2018 && cd sat2018
mkdir -p binaries
base_url="http://sat2018.forsyte.tuwien.ac.at/solvers/main_and_glucose_hack/" 

solvers=(
COMiniSatPS_Pulsar_drup.zip
CaDiCaL.zip
Candy.zip
GHackCOMSPS_drup.zip
Glucose_Hack_Kiel_fastBVE.zip
Lingeling.zip
MapleCOMSPS_CHB_VSIDS_drup.zip
MapleCOMSPS_LRB_VSIDS_2_drup.zip
MapleCOMSPS_LRB_VSIDS_drup.zip
MapleLCMDistChronoBT.zip
Maple_CM.zip
Maple_CM_Dist.zip
Maple_CM_ordUIP+.zip
Maple_CM_ordUIP.zip
Maple_LCM+BCrestart.zip
Maple_LCM+BCrestart_M1.zip
Maple_LCM_M1.zip
Maple_LCM_Scavel.zip
Maple_LCM_Scavel_200.zip
Minisat-v2.2.0-106-ge2dd095.zip
Riss7.1.zip
Sparrow2Riss-2018.zip
YalSAT.zip
abcdsat_r18.zip
cms55-main-all4fixed.zip
expGlucose.zip
expMC_LRB_VSIDS_Switch.zip
expMC_LRB_VSIDS_Switch_2500.zip
expMC_VSIDS_LRB_Switch_2500.zip
gluHack.zip
glu_mix.zip
glucose-3.0D-patched.zip
glucose-3.0_PADC_3.zip
glucose-3.0_PADC_10.zip
glucose3.0.zip
glucose4.2.1.zip
inIDGlucose.zip
smallsat.zip
varisat.zip)

for i in "${solvers[@]}"; do 
    wget "$base_url$i"
    unzip "$i"
    cd ${i%.*}
    sh "./starexec_build"
    cd ..
done