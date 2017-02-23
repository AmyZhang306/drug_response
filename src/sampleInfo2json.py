#zhm 2017-02-02

#python library
import sys
import json
import csv
import argparse
import copy
from acjson_acpipe.acjson import acbuild


def sample2acjson (sampletsv, s_layout_time0, s_layout_exp, s_runtype="sample2acjson"):
    ''' Transfer the tsv file of sample information into acjson format.

    Args:
        drugtsv: the drug information file using the following format, first row is the header 
            line (Plate Barcode	Image Barcode	Exp Time	Time Unit	Image Barcode of Time0	Well Number of Time0	Cell Line	Cell Number	Unit of Cell Number),
            then the data lines.
        s_layouttype: string ("plateNum|max_drugNum")
        s_runtype: input the name of this function, it's an argument for the "acbuild" function
    
    Returns:
        return the acjson of sample information
    '''

    #read in the tsv file of drug information
    with open (sampletsv, "r") as in_file:
        h_samp=csv.reader(in_file, delimiter="\t")
        header=next(h_samp)

        d_time0={}
        last_time0_barcode=""
        for lst_info in h_samp:
            (imageBar, time, timeUnit, imageBar_time0, wellNum_time0, cellLine, conc, concUnit)=lst_info[1:]
            #if going to a new time 0 plate, write the old one down 
            if (last_time0_barcode and (imageBar_time0 != last_time0_barcode)):
                ac_time0=acbuild(s_layouttype=s_layout_time0, s_runid=last_time0_barcode, s_runtype=s_runtype)
                for key in ac_time0.keys():
                    if (isinstance(ac_time0[key], dict)):
                        wellNum=ac_time0[key]["s|i"]
                        try:
                            ac_time0[key]["sample"]=d_time0[wellNum]
                        except KeyError:
                            next
               	#write out the time0 plate
               	outfile_time0=args.d + "/" + ac_time0["acid"]
               	f_time0=open(outfile_time0, "w")
               	json.dump(ac_time0, f_time0, indent=4, sort_keys=True)
               	f_time0.close()
               	d_time0={}
            #create the dictionary of time0
            lst_wellNum=wellNum_time0.split(";") 
            for well in lst_wellNum:
                try:
                    d_well0=d_time0[well] 
                except KeyError:
                    d_well0={}
                try:
                    d_cellLine0=d_well0[cellLine]
                except KeyError:
                    d_cellLine0={}
                    d_cellLine0.update({"conc": conc})
                    d_cellLine0.update({"concUnit": concUnit})
                    d_cellLine0.update({"time": 0})
                    d_cellLine0.update({"timeUnit": timeUnit})
                d_well0.update({cellLine: d_cellLine0})
                d_time0.update({well: d_well0})
            last_time0_barcode=imageBar_time0

            #create the dictionary of experiment time
            d_ExpTime={}
            try:
                d_ExpSamp=d_ExpTime[cellLine]
            except KeyError:
                d_ExpSamp={}
                d_ExpSamp.update({"conc": conc})
                d_ExpSamp.update({"concUnit": concUnit})
                d_ExpSamp.update({"time": time})
                d_ExpSamp.update({"timeUnit": timeUnit})
            d_ExpTime.update({cellLine: d_ExpSamp})
            ac_exp=acbuild(s_layouttype="1|1", s_runtype=s_runtype, s_runid=imageBar)
            ac_exp["1"]["sample"]=d_ExpTime
            #write the experiment plate down
            outfile_exp=args.d + "/" + ac_exp['acid']
            f_exp=open(outfile_exp, "w")
            json.dump(ac_exp, f_exp, indent=4, sort_keys=True)
            f_exp.close()

        #write the last time0 file down
        ac_time0=acbuild(s_layouttype=s_layout_time0, s_runid=last_time0_barcode, s_runtype=s_runtype)
        for key in ac_time0.keys():
            if (isinstance(ac_time0[key], dict)):
                wellNum=ac_time0[key]["s|i"]
                try:
                    ac_time0[key]["sample"]=d_time0[wellNum]
                except KeyError:
                    next
       	#write out the time0 plate
       	outfile_time0=args.d + "/" + ac_time0["acid"]
       	f_time0=open(outfile_time0, "w")
       	json.dump(ac_time0, f_time0, indent=4, sort_keys=True)
       	f_time0.close()

if __name__=="__main__":

    '''
    Usage: drugInfo2acjson.py --tsv input --layout --acjson output     
    '''

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--tsv', help='input the tsv file of sample information')
    parser.add_argument('--layout_time0', type=str, help='input the layout of time0 plate like 384 wells "16|24" ')
    parser.add_argument('--layout_exp', type=str, help='input the layout of drug plate like 384 wells "16|24" ')
    parser.add_argument('--d', help='directory or output files')

    args = parser.parse_args()

    #run the subfunction
    sample2acjson(sampletsv=args.tsv, s_layout_time0=args.layout_time0, s_layout_exp=args.layout_exp)
