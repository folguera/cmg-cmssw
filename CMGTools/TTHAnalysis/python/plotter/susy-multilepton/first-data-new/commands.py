#!/usr/bin/env python

ODIR="~/www/25ns_run2015d_upto258750"
MYTREEDIR="/data1/p/peruzzi/TREES_74X_161015_MiniIso"
MYLUMI="1.26388"

EXE="python mcPlots.py"
WDIR="susy-multilepton/first-data-new"
COMMOPT='--s2v --tree treeProducerSusyMultilepton --FMC sf/t {P}/1_puWeights_v1_run2015D_upto258714/evVarFriend_{cname}.root -W vtxWeight --noErrorBandOnRatio  --rspam "%(lumi) (13 TeV)  " --lspam "#bf{CMS} #it{Preliminary}" --legendBorder=0 --legendFontSize 0.055 --legendWidth=0.35 --showRatio --maxRatioRange 0 2 --showRatio --poisson -j 8 -f --sp ".*"'

SELECTIONS=["ZtoEE","ZtoMuMu","ttbar","Wl","Zl","ttbar_semiLeptonic"]

for SEL in SELECTIONS:
    print '#'+SEL
    MCA = 'mca_13tev_%s.txt'%SEL if SEL in ['Wl','Zl','ttbar_semiLeptonic'] else 'mca_13tev.txt'
    MYMCC = '--mcc %s/mcc_%s.txt'%(WDIR,SEL)
#    print '%s %s/%s %s/cuts_%s.txt %s/plots_%s.txt %s -P %s -l %s %s --scaleSigToData --pdir %s/%s/ScaleSigToData'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,SEL,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)
    COARSE = '_coarse' if SEL in ['Wl','Zl','ttbar_semiLeptonic'] else ''
    print '%s %s/%s %s/cuts_%s.txt %s/plots_lepquantities%s.txt %s -P %s -l %s %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COARSE,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)
    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s -l %s %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYLUMI,MYMCC,ODIR,SEL)


SELECTIONS=["ttbar_application"]
for SEL in SELECTIONS:
    print '#'+SEL
    MCA = 'mca_13tev.txt'
    print '%s %s/%s %s/cuts_%s.txt %s/plots_eventquantities.txt %s -P %s -l %s --pdir %s/%s/ScaleToLumi'%(EXE,WDIR,MCA,WDIR,SEL,WDIR,COMMOPT,MYTREEDIR,MYLUMI,ODIR,SEL)
