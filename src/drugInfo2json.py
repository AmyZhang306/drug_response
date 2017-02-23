#zhm 2017-02-02

#python library
import sys
import json
import csv
import argparse
from acjson_acpipe.acjson import acbuild


def drugInfo2acjson (drugtsv, s_layouttype, s_runid, s_runtype="drugInfo2acjson"):
    ''' Transfer the tsv file of drug information into acjson format.

    Args:
        drugtsv: the drug information file using the following format, first row is the header 
            line (Compound	Plate	DrugNumber	Concentration	ConcentrationUnit	Time	TimeUnit),
            then the data lines.
        s_layouttype: string ("plateNum|max_drugNum")
        s_runtype: input the name of this function, it's an argument for the "acbuild" function
    
    Returns:
        return the acjson of drug information
    '''

    #create the template of acjson
    ac_template=acbuild(s_layouttype=s_layouttype, s_runtype=s_runtype, s_runid=s_runid)

    #read in the tsv file of drug information
    with open (drugtsv, "r") as in_file:
        h_drug=csv.reader(in_file, delimiter="\t")
        header=next(h_drug)
        i_num=0
        for lst_info in h_drug:
            i_num+=1
            s_num=str(i_num)
            (compound, plate, drugNum, conc, concUnit, time, timeUnit)=lst_info
            #split them if there are more than one compound
            lst_compound=compound.split('_')
            lst_conc=conc.split('_')
            #put the drug information into the perturbation part
            d_perturb={}
            for i in range(len(lst_compound)):
                try:
                    d_comp=d_perturb[lst_compound[i]]
                except KeyError:
                    d_comp={}
                    d_comp.update({"conc": lst_conc[i]})
                    d_comp.update({"concUnit": concUnit})
                    d_comp.update({"time": time})
                    d_comp.update({"timeUnit": timeUnit})
                d_perturb.update({lst_compound[i]: d_comp})
            ac_template[s_num]["perturbation"]=d_perturb

    #return
    return ac_template  


if __name__=="__main__":

    '''
    Usage: drugInfo2acjson.py --tsv input --layout --acjson output    
    '''

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--tsv', help='input the tsv file of drug information')
    parser.add_argument('--layout', type=str, help='input the total plate number and max drug number like this "plateNum|drugNum" ')
    parser.add_argument('--n', help='outfile name without the suffix')
    parser.add_argument('--d', help='output directory')

    args = parser.parse_args()

    #run the subfunction
    drug_acjson=drugInfo2acjson(drugtsv=args.tsv, s_layouttype=args.layout, s_runid=args.n)
    #write out
    outfile=args.d + "/" + drug_acjson['acid']
    f=open(outfile, "w") # args.acjson  
    json.dump(drug_acjson, f, indent=4, sort_keys=True)
    f.close()
