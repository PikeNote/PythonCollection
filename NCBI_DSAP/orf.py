# divide the DNA into sections from the specific starting point
def sectioner(DNA, start):
  dnaList = [];
  section = ""
  i = 0
  limit = 0
  if (start > 0):
    limit = start
  for x in DNA:
  #  print("\nCurrent X: " + x)
  #  print("Current I: ", end = "")
  #  print(i)
    i += 1
    section += x
    if (limit == 1):
    #  print("Removed Section: ")
    #  print(section[start - 1:])
      section = section[(start - 1):]
      i = 0
      limit += 3
    elif (limit == 2 and len(section) > 1):
    #  print("Removed Section (two): ")
    #  print(section[start - 1:])
      section = section[(start - 1):]
      i = 0
      limit += 2
    if i % 3 == 0:
      dnaList.append(section)
    #  print("Section: " + section)
      section = ""
  return dnaList;
      
# turn the sectioned DNA sequence into codons
def dnaTocodon(dnaList):
  codonList  = [];
  for x in dnaList:
    match x:
      # Ala
      case "GCT" | "GCC" | "GCA" | "GCG":
        codonList.append("A")
      # Cys
      case "TGT" | "TGC":
        codonList.append("C")
      # Asp
      case "GAT" | "GAC":
        codonList.append("D")
      # Glu
      case "GAA"| "GAG":
        codonList.append("E")
      # Phe
      case "TTT" | "TTC":
        codonList.append("F")
      # Gly
      case "GGT" | "GGC" | "GGA" | "GGG":
        codonList.append("G")
      # His
      case "CAT" | "CAC":
        codonList.append("H");
      # Ile
      case "ATT" | "ATC" | "ATA":
        codonList.append("I")
      # Lys
      case "AAA" | "AAG":
        codonList.append("K")
      # Leu
      case "TTA" | "TTG" | "CTT" | "CTC" | "CTA" | "CTG":
        codonList.append("L")
      # Met (Start Codon)
      case "ATG":
        codonList.append("M")
      # Asn
      case "AAT" | "AAC":
        codonList.append("N")
      # Pro
      case "CCT" | "CCC" | "CCA" | "CCG":
        codonList.append("P")
      # Gln
      case "CAA" | "CAG":
        codonList.append("Q")
      # Arg
      case "CGT" | "CGC" | "CGA" | "CGG" | "AGA" | "AGG":
        codonList.append("R")
      # Ser
      case "TCT" | "TCC" | "TCA" | "TCG" | "AGT" | "AGC":
        codonList.append("S")
      # Thr
      case "ACT" | "ACC" | "ACA" | "ACG":
        codonList.append("T")
      # Val
      case "GTT" | "GTC" | "GTA" | "GTG":
        codonList.append("V")
      # Trp
      case "TGG":
        codonList.append("W")
      # Tyr
      case "TAT" | "TAC":
        codonList.append("Y")
      # Stop Codon
      case "TAA" | "TAG" | "TGA":
        codonList.append("*")
      case _:
        continue
  return codonList

# section the codons from the first met to the next stop codon
def finalSequence(codonList):
  firstM = 0
  finalSeq = []
  for x in codonList:
    if (x == 'M' and firstM == 0):
      firstM += 1
    if (firstM == 1):
      finalSeq.append(x);
  return finalSeq;
      

# which reading frame is the best
def comparison(frameOne, frameTwo, frameThree):
  lengthOne = len(frameOne)
  lengthTwo = len(frameTwo)
  lengthThree = len(frameThree)
  if (lengthOne > lengthTwo and lengthOne > lengthThree):
    print("Reading Frame 01 is the best.")
  elif(lengthTwo > lengthOne and lengthTwo > lengthThree):
    print("Reading Frame 02 is the best.")
  elif(lengthThree > lengthOne and lengthThree > lengthTwo):
    print("Reading Frame 03 is best.")