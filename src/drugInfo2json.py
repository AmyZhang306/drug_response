#!/usr/local/bin/python3

import sys
import json
import csv
import textwrap

def drugInfo2json (drugtsv, drugjson):
    #read in the drug information file
    with open (drugtsv, "r") as in_file:
        h_drug=csv.reader(in_file, delimiter="\t")
        header=next(h_drug)
        d_drugInfo={}
        for lst_info in h_drug:
            (compound, plate, drugNum, conc, concUnit, time, timeUnit)=lst_info
            #create the dictionary on plate level
            try:
                d_plate=d_drugInfo[plate]
            except KeyError:
               d_plate={}
            #create the dictionary on drugNum level
            try:
                d_drugNum=d_plate[drugNum]
            except KeyError:
                d_drugNum={}
            #create the dictionary on compound level
            lst_compound=compound.split('_')
            lst_conc=conc.split('_')
            for i in range(len(lst_compound)):
                try:
                    d_comp=d_drugNum[lst_compound[i]]
                except KeyError:
                    d_comp={}
                    d_comp.update({"conc": lst_conc[i]})
                    d_comp.update({"concUnit": concUnit})
                    d_comp.update({"time": time})
                    d_comp.update({"timeUnit": timeUnit})
                d_drugNum.update({lst_compound[i]: d_comp})
            #update the d_plate and d_drugInfo
            d_plate.update({drugNum: d_drugNum})
            d_drugInfo.update({plate: d_plate})
    #output the dictionary to json file
    outfile=drugjson
    f=open(outfile, "w")
    json.dump(d_drugInfo, f)
    f.close()

def main():
    '''
    Usage: drugInfo2json.py infile.tsv outfile.json

    Function: Transfer the drug information table file into json format.

    The input tsv file must meet the following requirements:

    - The first row contains column names as following:
    Compound	Plate	DrugNumber	Concentration	ConcentarionUnit	Time	TimeUnit
    '''

    if '-h' in sys.argv or '--help' in sys.argv:
        print (textwrap.dedent(main.__doc__))
        return
    #transfer the tsv file to json file
    drugInfo2json(sys.argv[1], sys.argv[2])
    

if __name__=="__main__":
    main()
