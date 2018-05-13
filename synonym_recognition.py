from tripple_processing import *


def get_candidates(matrix):
    non_zero_ind_matrix = [np.nonzero(row)[0] for row in matrix]
    non_zero_ind_matrix = [row for row in non_zero_ind_matrix if len(row) > 1]
    non_zero_ind_matrix = [list(itertools.combinations(row, 2)) for row in non_zero_ind_matrix]
    pairs = {}
    for row in non_zero_ind_matrix:
        for pair in row:
            if pair not in pairs:
                pairs[pair] = 1
            else:
                pairs[pair] += 1

    return pairs


def get_subject_verb_candidates(triples):
    s_v_matrix = subject_verb_frequency_matrix(triples)
    candidates = get_candidates(s_v_matrix)
    return candidates


def get_verb_object_candidates(triples):
    v_o_matrix = verb_object_frequency_matrix(triples)
    candidates = get_candidates(v_o_matrix)
    return candidates


def get_filtered_candidates(candidates, min):
    dict = {}
    for key, value in candidates.iteritems():
        if value >= min:
            dict[key] = value

    return dict


def print_subject_candidate_names(candidate, triples):
    subjects = get_subjects(triples)
    print '{0} - {1}'.format(subjects[candidate[0]], subjects[candidate[1]])


def print_object_candidate_names(candidate, triples):
    subjects = get_objects(triples)
    print '{0} - {1}'.format(subjects[candidate[0]], subjects[candidate[1]])
