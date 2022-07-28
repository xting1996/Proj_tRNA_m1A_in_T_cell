##计算RPM
##RPM一般用于比较不用control gene 长度，比如像tRNA这种数据的normalize
## RPM of gene = Number of reads mapped to a gene * 10^6 /Total number of mapped reads from given library

import pysam
import pandas as pd

import pysam
import argparse
parser = argparse.ArgumentParser(description="Count the bam RPM")
parser.add_argument("-i_bam", "--Input_bam_file",
                    help="Input the bam file ",required=True)
parser.add_argument("-output", "--Output_RPM_file",
                    help="Input the RPM form BAM file ",required=True)

ARGS = parser.parse_args()

input_art_file_path = ARGS.Input_bam_file
output_art_file_path = ARGS.Output_RPM_file

#f_out = open(output_art_file_path,"w")

data = pysam.AlignmentFile(input_art_file_path,"rb")




#data = pysam.AlignmentFile("AlkB_T0h_R1.BWA.sort.bam")

Total_mapped_reads = data.count()
test = data.get_index_statistics()

dict_name_coverage = {}
for i in range(0,len(test)):
    dict_name_coverage[test[i][0]] = test[i][1] 

df = pd.DataFrame.from_dict(dict_name_coverage,orient="index")
df.columns = ["ReadsNumber"]
df["RPM"] = df["ReadsNumber"] * pow(10,6) / Total_mapped_reads

df.to_csv(output_art_file_path,sep="\t")
