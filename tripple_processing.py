import numpy as np
import itertools


def filter_triples(triples):
    return [triple for triple in triples if triple.valid()]


# def subject_verb_frequency_matrix(triples):
#     matrix = [['']]
#     filtered_triples = filter_triples(triples)
#     for triple in filtered_triples:
#         if triple.subject not in matrix[0]:
#             matrix[0].append(triple.subject)
#         if triple.action not in matrix:
#             row = [triple.action]
#             s_ind = matrix[0].index(triple.subject)
#             if len(row) <= s_ind:
#                 row.append(1)
#             else:
#                 row[s_ind] += 1
#             matrix.append(row)
#
#     return matrix

def subject_verb_frequency_matrix(triples):
    filtered_triples = filter_triples(triples)
    verbs = get_verbs(filtered_triples)
    subjects = get_subjects(filtered_triples)
    matrix = np.zeros((len(verbs), len(subjects)))
    for triple in filtered_triples:
        v_ind = verbs.index(triple.action)
        s_ind = subjects.index(triple.subject)
        matrix[v_ind][s_ind] += 1

    return matrix


def get_subjects(triples):
    return list(set(triple.subject for triple in filter_triples(triples)))


def get_verbs(triples):
    return list(set(triple.action for triple in filter_triples(triples)))


def get_objects(triples):
    return list(set(triple.object for triple in filter_triples(triples)))


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


def get_filtered_candidates(candidates, min):
    dict = {}
    for key, value in candidates.iteritems():
        if value >= min:
            dict[key] = value

    return dict


def print_subject_candidate_names(candidate, triples):
    subjects = get_subjects(triples)
    print '{0} - {1}'.format(subjects[candidate[0]], subjects[candidate[1]])
