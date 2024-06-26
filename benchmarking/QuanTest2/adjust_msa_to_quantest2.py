#!/usr/bin/env python3

import numpy as np
import copy
import itertools
import sys
import ete3

import numpy as np
from Bio import AlignIO

# import CIAlign.cropSeq as cropSeq
# from AlignmentStats import find_removed_cialign

def writeOutfile(outfile, arr, nams, rmfile=None):
    '''
    Writes an alignment stored in a numpy array into a FASTA file.

    Parameters
    ----------
    outfile: str
        Path to FASTA file where the output should be stored
    arr: np.array
        Numpy array containing the cleaned alignment
    nams: list
        List of nams of sequences in the input alignment
    removed: set
        Set of names of sequences which have been removed
    rmfile: str
        Path to file used to log sequences and columns which have been removed

    Returns
    -------
    None

    '''
    out = open(outfile, "w")
    i = 0
    for nam in nams:
        out.write(">%s\n%s\n" % (nam, "".join(list(arr[i]))))
        i += 1
    out.close()

# helper function to read MSA from file into np array
def readMSA(infile, log=None, outfile_stem=None):
    '''
    Convert an alignment into a numpy array.

    Parameters
    ----------
    infile: string
        path to input alignment file in FASTA format
    log: logging.Logger
        An open log file object

    Returns
    -------
    arr: np.array
        2D numpy array in the same order as fasta_dict where each row
        represents a single column in the alignment and each column a
        single sequence.
    nams: list
        List of sequence names in the same order as in the input file
    '''

    formatErrorMessage = "The MSA file needs to be in FASTA format."
    nams = []
    seqs = []
    nam = ""
    seq = ""
    with open(infile) as input:
        for line in input:
            line = line.strip()
            if len(line) == 0:
                continue  # todo: test!
            if line[0] == ">":
                seqs.append([s.upper() for s in seq])
                nams.append(nam.upper())
                seq = []
                nam = line.replace(">", "")
            else:
                if len(nams) == 0:
                    if log:
                        log.error(formatErrorMessage)
                    print(formatErrorMessage)
                    exit()
                seq += list(line)
    seqs.append(np.array([s.upper() for s in seq]))
    nams.append(nam.upper())
    arr = np.array(seqs[1:])
    return (arr, nams[1:])


def find_removed_cialign(removed_file, arr, nams, keeprows=False):
    '''
    Reads the "_removed.txt" file generated by CIAlign to determine
    what CIAlign has removed from the original alignment.

    Replaces nucleotides removed by CIAlign with "!" in the array representing
    the alignment so that it is still possible to compare these alignments
    with uncleaned alignments in terms of knowing which columns and pairs
    of residues are aligned.

    ! characters are always counted as mismatches in comparisons between
    alignments.

    Also counts how many total characters were removed by CIAlign and
    how many non-gap characters.

    Parameters
    ----------
    removed_file: str
        Path to a CIAlign _removed.txt log file
    arr: np.array
        Numpy array containing the alignment represented as a 2D matrix, where
        dimension 1 is sequences and dimension 2 is columns
    nams: list
        List of names in the original alignment, in the same order as in the
        input and the sequence array (these should always be the same).

    Returns
    -------
    cleanarr:
        2D numpy array containing the alignment represented as a 2D matrix,
        where dimension 1 is sequences and dimension 2 is columns, with
        residues removed by CIAlign represented as !
        Fully removed sequences are removed from this array.
    cleannams:
        List of names in the output alignment, with any sequences fully
        removed by CIAlign removed.
    '''
    # Read the CIAlign _removed.txt log file
    lines = [line.strip().split("\t")
             for line in open(removed_file).readlines()]
    removed_count_total = 0
    removed_count_nongap = 0
    # Make an empty dictionary
    D = {x: set() for x in nams}
    for line in lines:
        func = line[0]
        if len(line) != 1:
            ids = line[-1].split(",")
        else:
            ids = []
        ids = [id.upper() for id in ids]
        # for crop_ends and remove_insertions columns are removed so keep
        # track of column numbers as integers
        if func in ['crop_ends', 'remove_insertions', 'other']:
            ids = [int(x) for x in ids]
        # crop_ends is only applied to some sequences so also
        # keep track of sequence names
        if func == "crop_ends":
            nam = line[1].upper()
            D[nam] = D[nam] | set(ids)
        # no need to remove insertions from sequences which were removed
        # completely later
        elif func == "remove_insertions":
            for nam in nams:
                # nam = nam.upper()
                if D[nam] != "removed":
                    D[nam] = D[nam] | set(ids)
        # remove divergent and remove short remove the whole sequence
        elif func in ["remove_divergent", "remove_short", "otherc"]:
            for nam in ids:
                D[nam] = "removed"
        elif func == "other":
            for nam in nams:
                if D[nam] != "removed":
                    D[nam] = D[nam] | set(ids)
    # make copies of the arrays (because I'm never quite sure when
    # python makes links rather than copies)
    cleannams = copy.copy(nams)
    cleannams = np.array([x.upper() for x in cleannams])
    cleanarr = copy.copy(arr)

    # iterate through everything that has been changed
    for nam, val in D.items():
        which_nam = np.where(cleannams == nam)[0][0]
        # remove the removed sequences from the array
        if val == "removed":
            # keep track of the number of removed positions
            removed_count_total += len(cleanarr[which_nam])
            # keep track of the number of removed residues
            removed_count_nongap += sum(cleanarr[which_nam] != "-")

            # only keep names of sequences which are not removed
            cleannams = np.append(cleannams[:which_nam],
                                  cleannams[which_nam + 1:])

            # only keep the sequences which are not removed
            cleanarr = np.vstack([cleanarr[:which_nam],
                                  cleanarr[which_nam+1:]])
            # remove them from the input temporarily just to keep the shapes
            # the same
            arr = np.vstack([arr[:which_nam], arr[which_nam+1:]])
        else:
            # replace column substitutions with !
            which_pos = np.array(sorted(list(val)))
            if len(which_pos) != 0:
                cleanarr[which_nam, which_pos] = "!"

    removed_count_total += np.sum(cleanarr == "!")

    # sometimes gaps are removed - make these gaps in the output rather than
    # !s
    cleanarr[arr == "-"] = "-"
    removed_count_nongap += np.sum(cleanarr == "!")
    return (cleanarr, cleannams, removed_count_total, removed_count_nongap)


msa_file = sys.argv[1]
removed_file = sys.argv[2]
fake_outfile = sys.argv[3]

arr, nams = readMSA(msa_file)
arr = np.char.upper(arr)

(cleanarr, cleannams, removed_count_total, removed_count_nongap) = find_removed_cialign(removed_file, arr, nams)

writeOutfile(fake_outfile, cleanarr, cleannams)
