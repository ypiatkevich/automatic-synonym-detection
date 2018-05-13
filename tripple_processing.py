import numpy as np
import itertools


def s_v_filter(triples):
    return [triple for triple in triples if triple.s_v_valid()]


def v_o_filter(triples):
    return [triple for triple in triples if triple.v_o_valid()]


def s_v_o_filter(triples):
    return [triple for triple in triples if triple.s_v_o_valid()]


def subject_verb_frequency_matrix(triples):
    filtered_triples = s_v_filter(triples)
    verbs = get_verbs(filtered_triples)
    subjects = get_subjects(filtered_triples)
    matrix = np.zeros((len(verbs), len(subjects)))
    for triple in filtered_triples:
        v_ind = verbs.index(triple.action)
        s_ind = subjects.index(triple.subject)
        matrix[v_ind][s_ind] += 1

    return matrix


def subject_verb_id_matrix(triples):
    filtered_triples = s_v_filter(triples)
    verbs = get_verbs(filtered_triples)
    subjects = get_subjects(filtered_triples)
    matrix = []
    for i in range(len(verbs)):
        row = []
        for j in range(len(subjects)):
            el = []
            row.append(el)

        matrix.append(row)

    for triple in filtered_triples:
        v_ind = verbs.index(triple.action)
        s_ind = subjects.index(triple.subject)
        matrix[v_ind][s_ind].append(triple.id)

    return matrix


def verb_object_frequency_matrix(triples):
    filtered_triples = v_o_filter(triples)
    verbs = get_verbs(filtered_triples)
    objects = get_objects(filtered_triples)
    matrix = np.zeros((len(verbs), len(objects)))
    for triple in filtered_triples:
        v_ind = verbs.index(triple.action)
        o_ind = objects.index(triple.object)
        matrix[v_ind][o_ind] += 1

    return matrix


def get_subjects(triples):
    return list(set(triple.subject for triple in triples))


def get_verbs(triples):
    return list(set(triple.action for triple in triples))


def get_objects(triples):
    return list(set(triple.object for triple in triples))
