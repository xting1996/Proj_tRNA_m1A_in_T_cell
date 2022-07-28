##################################################
##xiaotingzhang@pku.edu.cn 
##2019-12-22
##For m1A mismatch file format,merge the different samples
##The input file may should be tagged that IP the Input flag.
##################################################
###import
import pandas as pd
import sys
import numpy as np
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
import argparse
parser = argparse.ArgumentParser(description="Merge the Input-IP mismatch files")
parser.add_argument("-Input","--Input_AlkB",
		nargs="?",type=argparse.FileType('r'),default=sys.stdin,
		help="Input file(AlkB treat)")
parser.add_argument("-IP","--IP",
		nargs="?",type=argparse.FileType('r'),default=sys.stdin,
		help="IP file (No AlkB treat)")
parser.add_argument("-Output","--Output_file",
		nargs="?",type=argparse.FileType("w"),default=sys.stdout,
		help="Merged Output File name")
parser.add_argument("-FC","--FoldChange",
		type=int,default=0,
		help="Filter the IP & Input flodchange greater than X (default 0)")
parser.add_argument("-diff","--diff",
		type=int,default=0,
		help="Filter the IP & Input diff greater than X (default 0)")
parser.add_argument("-coverage","--coverage_depth",
		type=int,default=0,
		help="Filter the Input & IP coverage greater than X (default 0)")

args = parser.parse_args()

Input_file = args.Input_AlkB
IP_file = args.IP
Output_file = args.Output_file
FC = args.FoldChange
Diff = args.diff
coverage = args.coverage_depth

"""
Input : IP---> AlkB treat
IP: IP
"""

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
Input = pd.read_csv(Input_file,sep='\t')
IP = pd.read_csv(IP_file,sep='\t')
##index
Input['chr_index_base']=Input['gene_id']+"_"+Input['pos'].apply(str)+"_"+Input["refer_base"]
IP['chr_index_base']=IP['gene_id']+"_"+IP['pos'].apply(str)+"_"+IP['refer_base']
##merge
Input_IP = pd.merge(Input,IP,on='chr_index_base',how="inner",suffixes=("_input","_IP"))
##tidy format
Input_IP.drop(columns=["gene_id_IP","pos_IP","refer_base_IP"],inplace=True)
Input_IP = Input_IP[["chr_index_base","gene_id_input","pos_input","refer_base_input","coverage_input","A_input","T_input","C_input","G_input","mismatch%_input","coverage_IP","A_IP","T_IP","C_IP","G_IP","mismatch%_IP"]]
##FC & diff
Input_IP['FC']=Input_IP['mismatch%_IP']/Input_IP["mismatch%_input"]
Input_IP['diff']=Input_IP['mismatch%_IP']-Input_IP["mismatch%_input"]
##filter
Output = Input_IP[(Input_IP.FC > FC) & (Input_IP['diff'] > Diff) & (Input_IP.coverage_input > coverage) & (Input_IP.coverage_IP > coverage)]
#Output = Output[Output["diff"] > Diff]
##out
Output.to_csv(Output_file,sep="\t",index=False)
