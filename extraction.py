from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree, Tree
from svo import *
import Queue

parser = StanfordParser()


def get_tree(sentence):
    t = list(parser.raw_parse(sentence))[0]
    return ParentedTree.convert(t)[0]


def move_to_last_np(tree):
    node = None
    for child in tree:
        if child.label() in ['NP']:
            node = child

    if node is not None:
        return move_to_last_np(node)
    else:
        return tree


def move_to_last_vp(tree):
    node = None
    for child in tree:
        if child.label() in ['VP']:
            node = child

    if node is not None:
        return move_to_last_vp(node)
    else:
        return tree


def get_subject(tree):
    subj_np_tree = get_subject_np_paren_tree(tree)

    subj_tree = None
    subj = None

    if subj_np_tree is not None:
        subj_tree = get_subject_tree(subj_np_tree)

    if subj_tree is not None:
        subj = get_subject_value(subj_tree)

    return subj


def get_subject_params(tree):
    subj_np_tree = get_subject_np_paren_tree(tree)

    subj_tree = None
    params = []

    if subj_np_tree is not None:
        subj_tree = get_subject_tree(subj_np_tree)

    if subj_tree is not None:
        params = get_subject_param_values(subj_tree)

    return params


def get_subject_np_paren_tree(tree):
    q = Queue.LifoQueue()
    q.put(tree)
    while not q.empty():
        cur_tree = q.get()

        labels = get_sibling_labels(cur_tree)
        if ('WHNP' in labels) and ('S' in labels):
            cur_tree = cur_tree.parent()
            return cur_tree

        if cur_tree.label() in ['NP']:
            cur_tree = cur_tree.parent()
            return cur_tree

        for sub in cur_tree:
            if not isinstance(sub[0], unicode):
                if sub.label() not in ['VP']:
                    q.put(sub)


def get_subject_tree(tree):
    for child in tree:
        if child.label() in ['NP', 'PP']:
            node = move_to_last_np(child)
            return node


def get_subject_value(tree):
    labels = get_sibling_labels(tree)
    if labels.__contains__('CC'):
        ind = labels.index('CC')
    else:
        ind = len(tree)

    for i in range(ind, 0, -1):
        if tree[i - 1].label() in ['NN', 'NNS', 'PRP', 'NNP', 'NNPS']:
            return tree[i - 1][0]


def get_subject_param_values(tree):
    labels = get_sibling_labels(tree)
    if labels.__contains__('CC'):
        ind = labels.index('CC')
    else:
        ind = len(tree)

    for i in range(ind, 0, -1):
        if tree[i - 1].label() in ['NN', 'NNS', 'PRP', 'NNP', 'NNPS']:
            subj_ind = i - 1
            return [(tree[i].label(), tree[i][0]) for i in range(ind) if
                    i != subj_ind and isinstance(tree[i][0], unicode) and tree[i].label() not in ['DT', 'JJS', 'JJR',
                                                                                                  'CD']]


def find_action(tree):
    if tree.label() in ['SBAR']:
        for sub in tree:
            if sub.label() in ['S']:
                return get_action(sub)
    else:
        return get_action(tree)


def get_action(tree):
    for child in tree:
        if child.label() in ['VP']:
            node = move_to_last_vp(child)
            for sibling in node:
                if sibling.label() in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                    return sibling[0]


def get_object_np_tree(tree):
    if tree.label() in ['SBAR']:
        for sub in tree:
            if sub.label() in ['S']:
                return sub
    else:
        return tree


def get_object_tree(tree):
    for child in tree:
        if child.label() in ['VP']:
            node = move_to_last_vp(child)
            return node


def get_object(tree):
    obj_np_tree = get_object_np_tree(tree)

    obj_tree = None
    obj = None

    if obj_np_tree is not None:
        obj_tree = get_object_tree(tree)

    if obj_tree is not None:
        obj = get_subject(obj_tree)

    return obj


def get_object_params(tree):
    obj_np_tree = get_object_np_tree(tree)

    obj_tree = None
    blah_tree = None
    params = []

    if obj_np_tree is not None:
        obj_tree = get_object_tree(tree)

    if obj_tree is not None:
        blah_tree = get_subject_tree(obj_tree)

    if blah_tree is not None:
        params = get_subject_param_values(blah_tree)

    return params


def check_np_vp_in_s(tree):
    for sub in tree:
        if sub.label() in ['NP', 'VP']:
            return True

    return False


def get_sibling_labels(tree):
    return [t.label() for t in tree]


def get_direct_descendants(tree):
    return [(t.label(), t[0]) for t in tree]


def find_trees_to_analyze(tree):
    trees = []
    q = Queue.LifoQueue()
    q.put(tree)
    while not q.empty():
        cur_tree = q.get()
        if check_tree(cur_tree):
            trees.append(cur_tree)

        for sub in cur_tree:
            if not isinstance(sub[0], unicode):
                q.put(sub)

    return trees


def check_tree(tree):
    labels = get_sibling_labels(tree)
    if ('NP' in labels) and ('VP' in labels):
        return True
    elif ('WHNP' in labels) and ('S' in labels):
        return True
    else:
        return False


def find_triple(tree):
    subject = get_subject(tree)
    subject_params = get_subject_params(tree)
    action = find_action(tree)
    object = get_object(tree)
    object_params = get_object_params(tree)
    svo = SVO(subject, subject_params, action, [], object, object_params)
    return svo


def find_triples(sentence):
    triples = []
    t = get_tree(sentence)
    # t.pretty_print()
    trees = find_trees_to_analyze(t)
    for tree in trees:
        tree.pretty_print()
        svo = find_triple(tree)
        print svo.__str__()
        triples.append(svo)

    return triples
