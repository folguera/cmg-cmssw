#!/bin/bash
TMPDIR=$PWD
#### ENV
AREA=/afs/cern.ch/user/g/gpetrucc/ttH/CMGTools/CMSSW_5_3_5/src/CMGTools/TTHAnalysis/cfg/fastSim
cd $AREA
export SCRAM_ARCH=slc5_amd64_gcc462
eval $(scramv1 runtime -sh)
#### CREATE CFG
INFILE=$1
OUTFILE=$(dirname $INFILE)/cmgTuple_2.$(basename $INFILE)
EXTRA1=""
EXTRA2=""
if [[ "$2" == "--split" ]]; then
   JOB=$3;
   EVENTS=$4;
   SKIP=$(( ($JOB - 1) * $EVENTS ))
   EXTRA1="process.source.skipEvents = cms.untracked.uint32($SKIP)"
   EXTRA2="process.maxEvents.input = cms.untracked.int32($EVENTS)"
   echo "Extra lines: "
   echo ">>>  $EXTRA1"
   echo ">>>  $EXTRA2"
   OUTFILE=${OUTFILE/.root/.job$JOB.root}
   echo "New outfile: $OUTFILE"
fi

OUTBASE=$(basename $INFILE .root)
echo "Will read from $INFILE and write to $OUTFILE";
if echo $INFILE | grep -q -v ^/store/; then
    INFILE="file:$INFILE";
fi

JOB=$TMPDIR/FASTSIM_CMG.cfg.py

cat $AREA/FASTSIM_CMG_expanded.py  > $JOB
echo "process.maxEvents.input = -1"                              >> $JOB
echo "process.source.fileNames = [ '$INFILE' ]"                  >> $JOB
echo "getattr(process.subProcess, '_SubProcess__process').outcmg.fileName = '$TMPDIR/$OUTBASE.root'"   >> $JOB
cat >> $JOB <<_EOF_
## Scramble
import random
rnd = random.SystemRandom()
for X in process.RandomNumberGeneratorService.parameterNames_(): 
   if X != 'saveFileName': getattr(process.RandomNumberGeneratorService,X).initialSeed = rnd.randint(1,99999999)
$EXTRA1
$EXTRA2
_EOF_

cd $TMPDIR
cmsRun $JOB 2>&1 | tee FASTSIM_CMG_$OUTBASE.log
test -f $TMPDIR/$OUTBASE.root && cmsStageIn $TMPDIR/$OUTBASE.root $OUTFILE
gzip FASTSIM_CMG_$OUTBASE.log && cp FASTSIM_CMG_$OUTBASE.log.gz $AREA/jobs
