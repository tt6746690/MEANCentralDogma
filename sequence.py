import sys

# prints all possible protein sequence from 6 reading frames without particular distinction of the reading frames they might belong to.
CodChart = {
    'UUU': 'F',
    'UUC': 'F',
    'UUA': 'L',
    'UUG': 'L',

    'UCU': 'S',
    'UCC': 'S',
    'UCA': 'S',
    'UCG': 'S',

    'UAU': 'Y',
    'UAC': 'Y',
    'UAA': '*',
    'UAG': '*',

    'UGU': 'C',
    'UGC': 'C',
    'UGA': '*',
    'UGG': 'W',

    'CUU': 'L',
    'CUC': 'L',
    'CUA': 'L',
    'CUG': 'L',

    'CCU': 'P',
    'CCC': 'P',
    'CCA': 'P',
    'CCG': 'P',

    'CAU': 'H',
    'CAC': 'H',
    'CAA': 'Q',
    'CAG': 'Q',

    'CGU': 'R',
    'CGC': 'R',
    'CGA': 'R',
    'CGG': 'R',

    'AUU': 'I',
    'AUC': 'I',
    'AUA': 'I',
    'AUG': 'M',

    'ACU': 'T',
    'ACC': 'T',
    'ACA': 'T',
    'ACG': 'T',

    'AAU': 'N',
    'AAC': 'N',
    'AAA': 'K',
    'AAG': 'K',

    'AGU': 'S',
    'AGC': 'S',
    'AGA': 'R',
    'AGG': 'R',

    'GUU': 'V',
    'GUC': 'V',
    'GUA': 'V',
    'GUG': 'V',

    'GCU': 'A',
    'GCC': 'A',
    'GCA': 'A',
    'GCG': 'A',

    'GAU': 'D',
    'GAC': 'D',
    'GAA': 'E',
    'GAG': 'E',

    'GGU': 'G',
    'GGC': 'G',
    'GGA': 'G',
    'GGG': 'G'
}
# declare variables
protein = []
start = []
start_r = []
new_sequence = []
codons = ''
record = ''

def find_start_codon(rna_sequence):
    # this function inputs the RNA sequence in string and returns the position of A in AUG start codon.
    starter = []
    starter.append(-1)
    if len(rna_sequence) < 3:
        return starter
    else:
        for i in range(0, len(rna_sequence)):
            if rna_sequence[i] == 'A' and rna_sequence[i+1] == 'U' and rna_sequence[i+2] == 'G':
                starter.append(i)
                starter[0] = 0
            if i+3 == len(rna_sequence):
                break
        return starter

# opens file and converts DNA sequence to RNA sequence
#DNA_file = open("DNA.txt", )
#DNA_string = DNA_file.read()
#DNA_file.close()

#adapt for command line input with child process
DNA_string = str(sys.argv[1]).upper()
RNA_string = DNA_string.replace("T", "U")
RNA_string_r = RNA_string[::-1]

# finds the position of start codon
start = find_start_codon(RNA_string)
start_r = find_start_codon(RNA_string_r)
# loop through the length from start codon to the end of the sequence with interval of 3.
# append 1 letter of string to the variable protein
# check for stop codon

if start[0] == 0:
    for i in range(1, len(start)):
        protein.append('')
        for n in range(start[i], len(RNA_string), 3):
            codons = RNA_string[n: n+3]
            if (len(codons) != 3) or (CodChart[codons] == "*"):
                break
            else:
                protein[len(protein)-1] += CodChart[codons]
        codons = ''
elif start[0] == -1:
    record = 'no start codon forward direction'
else:
    print('error!')
    
if start_r[0] == 0:
    for i in range(1, len(start_r)):
        protein.append('')
        for n in range(start_r[i], len(RNA_string_r), 3):
            codons = RNA_string_r[n: n+3]
            if (len(codons) != 3) or (CodChart[codons] == "*"):
                break
            else:
                protein[len(protein)-1] += CodChart[codons]
        codons = ''
elif start_r[0] == -1:
    record += 'no start codon reverse direction'
else:
    print('error!')

#print(record)
print(protein)







