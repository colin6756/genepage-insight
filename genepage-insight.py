#!/usr/bin/python
from __future__ import print_function
import os, math, datetime, requests, json, argparse, shutil, sys
import pandas as pd
import numpy as np

def mkfolder():
    '''Create a folder for each gapit results, copy result.csv and reference into that directory.
    All results will then be generated within it. The main function will take the script back into parent.'''
    print("Commenced at {}".format(datetime.datetime.now()))
    folder=str(args.file)[:-4]
    if os.path.exists(folder):
        shutil.rmtree(folder)
        os.mkdir(folder)
        shutil.copy(args.file, folder)
        shutil.copy(args.list, folder)
        os.chdir(folder)
    else:
        os.mkdir(folder)
        shutil.copy(args.file, folder)
        shutil.copy(args.list, folder)
        os.chdir(folder)
    # end of mkfolder()

def summary():
    '''Search on knetminer using information provided and truncate down to only relevant info'''
    with open(args.list, "r") as fk:
        pheno=[]
        for line in fk:
            pheno.append(line.rstrip())
        summary=pd.read_csv(args.file, sep="\t", header=None)
        summary.rename (
        columns={
            0:"GENE"
        }, inplace=True
        )
        genes=list(summary["GENE"])
        

        #creating knetminer genepage urls.
        network_view=[]
        keyw2 = "+OR+".join("({})".format(i.replace(" ", "+AND+")) for i in pheno)
        #print(keyw2)
        #define species
        if args.species == 1:
            species="riceknet"
        elif args.species == 2:
            species="wheatknet"
        elif args.species == 3:
            species="araknet"
        for i in genes:
            link="http://knetminer.rothamsted.ac.uk/{}/genepage?list={}&keyword={}".format(species, i, keyw2)
            r=requests.get(link)
            network_view.append(r.url)

        #obtaining knetscores for genes
        keyw1 = "%20OR%20".join("({})".format(i.replace(" ", "+AND+")) for i in pheno)
        print("The traits provided by user:")
        print(keyw1)
        print("The genes provided by user:")
        genestr=(",").join(genes)
        print(genestr)
        link="http://knetminer.rothamsted.ac.uk/{}/genome?".format(species)
        parameters={"keyword":keyw1, "list":genestr}
        r=requests.get(link, params=parameters)
        #print(r.text)

        #check if requests is successful
        if not r.ok:
                r.raise_for_status()
                sys.exit()
        else:
            print("request successful")

        #extract unicode string of geneTable decoded from json
        decoded=r.json()[u'geneTable'].split("\t")
        #remove space or newline at the end
        decoded=(decoded)[:-1]

        colnum=9
        #tabulate genetable into 9 columns.
        genetable=np.array(decoded).reshape(len(decoded)//colnum, colnum)
        genetable=pd.DataFrame(genetable[1:,:], columns=genetable[0,:])
        #print(genetable.shape)

        knetgenes=list(genetable[u'ACCESSION'])
        #print(knetgenes)
        knetscores=list(genetable[u'SCORE'])
        knetchro=list(genetable[u'CHRO'])
        knetstart=list(genetable[u'START'])

        #map genes to snps via a dictionary.
        knetdict=dict(zip(knetgenes, knetscores))
        print("Displaying knetscores for every gene.")
        print(knetdict)
        ordered_score=[]     
        for i in genes:
            #convert gene id to upper case to avoid sensitivity issues.
            i=i.upper()
            ordered_score.append(knetdict[i])
        
        summary[u'knetscore'] = ordered_score
        summary[u'chromosome']=knetchro
        summary[u'start_position']=knetstart
        summary[u'network_view']=network_view
        print("These are the genepage urls. Also available in results.txt.")
        for i in network_view:
            print(str(i))

        summary.to_csv("results.txt", sep="\t", index=False)
    #end of append_summary


def main():
    try:
        print("creating directory to output results")
        mkfolder()
    except:
        raise

    try:
        print("Searching with Knetminer for information relating to the genes.")
        summary()
    except:
        raise

    os.remove(args.list)
    os.remove(args.file)
    #end of main


if __name__ == "__main__":
    #creating parameters for the end-user.
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="Name of plain text file containing a list of genes.", type=str)
    parser.add_argument("list", help="a plain text file containing description of phenotypes of interest line by line")
    parser.add_argument("species", help="Choose an integer out of three to select the species of organism subjected to gwas. 1 being rice, 2 being wheat and 3 being arabidopsis", type=int)
    args = parser.parse_args()

    main()

    print("The entire pipeline finished at:")
    print(datetime.datetime.now())

    exit
