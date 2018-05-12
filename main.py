from extraction import *
from text_processing import *
from corpora_processing import *
from tripple_processing import *

# text = "An instruction set architecture (ISA) is the interface between the computer's software and hardware and also " \
#        "can be viewed as the programmer's view of the machine. Computers do not understand high-level programming " \
#        "languages such as Java, C++, or most programming languages used. A processor only understands instructions " \
#        "encoded in some numerical fashion, usually as binary numbers. Software tools, such as compilers, " \
#        "translate those high level languages into instructions that the processor can understand. Besides " \
#        "instructions, the ISA defines items in the computer that are available to a program-e.g. data types, " \
#        "registers, addressing modes, and memory. Instructions locate these available items with register indexes (or " \
#        "names) and memory addressing modes. The ISA of a computer is usually described in a small instruction manual, " \
#        "which describes how the instructions are encoded. Also, it may define short (vaguely) mnemonic names for the " \
#        "instructions. The names can be recognized by a software development tool called an assembler. An assembler is " \
#        "a computer program that translates a human-readable form of the ISA into a computer-readable form. " \
#        "Disassemblers are also widely available, usually in debuggers and software programs to isolate and correct " \
#        "malfunctions in binary computer programs. ISAs vary in quality and completeness. A good ISA compromises " \
#        "between programmer convenience (how easy the code is to understand), size of the code (how much code is " \
#        "required to do a specific action), cost of the computer to interpret the instructions (more complexity means " \
#        "more hardware needed to decode and execute the instructions), and speed of the computer (with more complex " \
#        "decoding hardware comes longer decode time). Memory organization defines how instructions interact with the " \
#        "memory, and how memory interacts with itself. During design emulation software (emulators) can run programs " \
#        "written in a proposed instruction set. Modern emulators can measure size, cost, and speed to determine if a " \
#        "particular ISA is meeting its goals. "
#
# text = "Many comparable societies, with different areas of interest, were founded in the nineteenth century (several " \
#        "of them also by Furnivall); not all have survived, and few have produced as many valuable volumes as EETS. " \
#        "The Society's success continues to depend very heavily on the loyalty of members, and especially on the " \
#        "energy and devotion of a series of scholars who have been involved with the administration of the Society - " \
#        "the amount of time and effort spent by those who over the years have filled the role of Editorial Secretary " \
#        "is immeasurable. Plans for publications for the coming years are well in hand: there are a number of " \
#        "important texts which should be published within the next five years. At present, notably because of the " \
#        "efforts of a series of Executive and Membership Secretaries, the Society's finances are in reasonable shape; " \
#        "but certain trends give concern to the Council. The Society's continuance is dependent on two factors: the " \
#        "first is obviously the supply of scholarly editions suitable to be included in its series; the second is on " \
#        "the maintenance of subscriptions and sales of volumes at a level which will cover the printing and " \
#        "distribution costs of the new and reprinted books. The normal copyright laws cover the Society's volumes. All " \
#        "enquiries about large scale reproduction, whether by photocopying or on the internet, should be directed to " \
#        "the Executive Secretary in the first instance. The Society's continued usefulness depends on its editors and " \
#        "on its ability to maintain its (re)printing programme - and that depends on those who traditionally have " \
#        "become members of the Society. We hope you will maintain your membership, and will encourage both the " \
#        "libraries you use and also other individuals to join. Membership conveys many benefits for you, and for the " \
#        "wider academic community concerned for the understanding of medieval texts. "

file_name = 'corpora/train.txt'

sents = read_file(file_name)
triples = []
for sent in sents:
    triples += get_triples(sent)

for triple in triples:
    print triple.__str__()

matrix = subject_verb_frequency_matrix(triples)

verbs = get_verbs(triples)
subjects = get_subjects(triples)

print subjects
for i in range(len(verbs)):
    print '{0} : {1}'.format(verbs[i], matrix[i])

print '\n'

candidates = get_candidates(matrix)
candidates = get_filtered_candidates(candidates, 2)
for key, value in candidates.iteritems():
    print_subject_candidate_names(key, triples)