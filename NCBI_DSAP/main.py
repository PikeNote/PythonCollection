import ncbi_blast;
import time;
import os;
import math;
import json;
import orf;
#operation, database, query
#valid programs:
#blastn, blastp, blastx, tblastn, tblastx

#valid database:
#Name 	Title 	Type
#nt 	Nucleotide collection 	DNA
#nr 	Non-redundant 	Protein
#est

def writeJson(path, data):
  f_json = open(path, "a");
  f_json.write(json.dumps(data));
  f_json.close();

def printResults(r,path):
  f = open(path, 'w')
  for p in r:
    desc = p["description"][0]
    hsps = p["hsps"]
    
    #f.write("Asscesion: " + desc["accession"] + "\n");
    #f.write("Title: " + desc["title"] + "\n")
    #f.write("Organism: " + desc["sciname"] + "\n")
    #f.write("Query Start: " + hsps[0]["qseq"][0].upper() + str(hsps[0]["query_from"]) + "\n")
    #f.write("Query End: " + hsps[len(hsps)-1]["qseq"][len(hsps[len(hsps)-1]["qseq"])-1].upper() +  str(hsps[len(hsps) - 1]["query_to"]) + "\n")
    #f.write("E-Value: " + str(hsps[0]["evalue"]) + "\n")

    print("Asscesion: " + desc["accession"],  file=f)
    print("Title: " + desc["title"],  file=f)
    print("Organism: " + desc["sciname"],  file=f)
    print("Query Start: " + hsps[0]["qseq"][0].upper() + str(hsps[0]["query_from"]),  file=f)
    print("Query End: " + hsps[len(hsps)-1]["qseq"][len(hsps[len(hsps)-1]["qseq"])-1].upper() +  str(hsps[len(hsps) - 1]["query_to"]),  file=f)
    print("E-Value: " + str(hsps[0]["evalue"]),  file=f)
    print()
  f.close();

def getBlastnResults(r):
  top3DifferentOrganisms = []
  existingOrgs = []

  for result in r:
    if (len(top3DifferentOrganisms) < 3):
      if (not result["description"][0]["sciname"] in existingOrgs):
        existingOrgs.append(result["description"][0]["sciname"])
        top3DifferentOrganisms.append(result)
  return top3DifferentOrganisms


valid_dna_seq = "ATGC"
valid_blasts = ["blastn", "blastp", "blastx", "tblastn", "tblastx"]

print("Please input your sequence: ")
seq = input().upper()

if (all(i in valid_dna_seq for i in seq)):
  print("Valid sequence detected!")
  name = str(int(time.time()));
  os.makedirs(name);

  if (len(seq) < 30):
    print("Short sequences may take longer to run!")

  # nt Blastn
  print("Running nt blastn sequence..")
  blastnNrData = ncbi_blast.blast("blastn", "nt", seq)
  writeJson(name+"/"+blastnNrData["rid"]+"_blastnNt_json.txt", blastnNrData)
  # print(blastnNrData)

  top3DifferentOrganisms = getBlastnResults(
    blastnNrData["BlastOutput2"][0]["report"]["results"]["search"]["hits"])
  print("Running est blastn sequence..")
  blastnEstData = ncbi_blast.blast("blastn", "est", seq)
  writeJson(name+"/"+blastnEstData["rid"]+"_blastnEst_json.txt", blastnEstData)
  
  print()
  print("Top 3 blastn results from different organisms (nt):")
  printResults(top3DifferentOrganisms, name+"/"+blastnNrData["rid"]+"_blastn.txt")
  print()


  top3DifferentOrganisms_Est = getBlastnResults(
    blastnEstData["BlastOutput2"][0]["report"]["results"]["search"]["hits"])
  print()
  print("Top 3 blastn results from different organisms (est):")
  print()
  printResults(top3DifferentOrganisms_Est, name+"/"+blastnEstData["rid"]+"_blastn.txt")
  print()
  
  print("Running blastx search..")
  blastXData = ncbi_blast.blast("blastx", "nr", seq)
  writeJson(name+"/"+blastXData["rid"]+"_blastx_json.txt", blastXData)
  top3DifferentOrganisms_blastX = getBlastnResults(
    blastnEstData["BlastOutput2"][0]["report"]["results"]["search"]["hits"])
  print("Top 3 blastx results from different organisms (est):")
  printResults(top3DifferentOrganisms_blastX, name+"/"+blastXData["rid"]+"_blastx.txt");

  print()

  print("Getting ORF data...")

  readingFrames = []
  final_seq = [];

  print("Reading frames:")
  f_frames = open(name+"/reading_frames.txt", "w");

  for i in range(3):
    sec_dna_frm = orf.sectioner(seq, i);
    dna_codon_frm = orf.dnaTocodon(sec_dna_frm);
    final_seq_frm = orf.finalSequence(dna_codon_frm)
    print("Frame " + str(i+1), file=f_frames);

    print("Codon: " + ''.join(dna_codon_frm), file=f_frames)
    final_seq.append(final_seq_frm)
    print("Final Seq: " + ''.join(final_seq_frm), file=f_frames)
    print("",file=f_frames);
    fromInd = i+1;
    toInd = len(dna_codon_frm)
    try:
      fromInd = (dna_codon_frm.index("M")+1)*3;
    except ValueError:
      pass;

    try:
      toInd = (dna_codon_frm.index("*")+1)*3;
    except ValueError:
      pass;
    
    print("From: " + seq[fromInd-1] + str(fromInd), file=f_frames);
    print("To: " + seq[toInd-1] + str(toInd), file=f_frames);
    print();
    print();

    f_frames.close();
  orf.comparison(final_seq[0],final_seq[1],final_seq[2]);

  
  

  #ncbi_blast.blast("blastn","nr/nt","CCGTTCCGGGCCGCAGTGAGTTGCTGTGGACGGACTCCGCCCGCACTGTCCTGCCCATTCTCAAGGAGCTCACGGCGGACGGCATCAGGGTCATGATTTACAGCGGGGACGTCGATGGTAAGGTTCCGGTGACCGCCACGCGGTACTCCGTGAACGCCCTCGGGCTGCCGGTGAAGACTCAGTGGTATCCGTGGAAGATCAGCGGCCAGGTGGGAGGCTACGCGGAAGAGTACGAGGGCAACTTGACGCTGGCAACAGTCAGAGGGGCGGGACTTCAGGTCCCGAGTAACAAGCCTTGGCCGGCGCTGGTCATCATTAGGTCCTTCATCGACGGAGAGCCTCTCCCTCCCTTCGAAACTGATAATCTCTAAGCTTCTCTCTCCCTCTCTCTCTCCCCCACTTTATTCCTCACTCTCCTTGAAGAATAAAATAAGGGAGAGCTGATGCTGCTCCCGGGGGACAATTTGAAGAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
