# Proj_tRNA_m1A_in_T_cell

Here ara some custom  scripts about how to get tRNA RPM and m1A modification.

### 1.For RPM 
`
python count_RPM.py -i_bam test.bam -output test.RPM.txt
`
### 2.For m1A modification

##### 1.using `samtools mpileup ` funtion to parse BAM info

`samtools mpileup --reference ${ref} test.sort.bam -d 1000000 -o test.sort.mpileup.xls`

##### 2.calling m1A info using Non-AlkB sample(IP) and AlkB-sample(Input)

 `
 python get_m1A_modification.py -Input test.AlkB.sort.mpileup.xls -IP test.Non-AlkB.sort.mpileup.xls -FC 3 -diff 10 -coverage 3 --Output test.m1A.txt
 `
