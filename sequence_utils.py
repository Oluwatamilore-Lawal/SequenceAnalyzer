CODON_TABLE = {
    'AUG': 'M', 'UUU': 'F', 'UUC': 'F',
    'UAA': '*', 'UAG': '*', 'UGA': '*'
}

VALID_CHARS = set('ATGCU')

def validate_sequence(seq):
    seq = seq.strip().replace('\n', '').replace(' ', '').upper()
    if not seq:
        raise ValueError('Sequence is empty')
    if any(c not in VALID_CHARS for c in seq):
        raise ValueError('Invalid characters in sequence')
    if 'T' in seq and 'U' in seq:
        raise ValueError('Sequence cannot contain both T and U')
    return seq

def detect_type(seq):
    return 'RNA' if 'U' in seq else 'DNA'

def nucleotide_count(seq):
    total = len(seq)
    counts = {n: seq.count(n) for n in VALID_CHARS if n in seq}
    return {n: {'count': c, 'percent': round(c/total*100, 2)} for n, c in counts.items()}

def translate_seq(seq):
    return seq.replace('T', 'U')

def transcribe_seq(seq):
    comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(comp.get(b, b) for b in seq)

def reverse_transcribe(seq):
    return seq.replace('U', 'T')

def to_protein(seq):
    rna = translate_seq(seq) if 'T' in seq else seq
    protein = []
    warning = None

    if len(rna) % 3 != 0:
        warning = 'Sequence length not divisible by 3'

    for i in range(0, len(rna) - 2, 3):
        codon = rna[i:i+3]
        protein.append(CODON_TABLE.get(codon, '?'))

    return protein, warning
