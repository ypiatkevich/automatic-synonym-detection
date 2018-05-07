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


def find_subject(tree):
    q = Queue.LifoQueue()
    q.put(tree)
    while not q.empty():
        cur_tree = q.get()

        labels = get_sibling_labels(cur_tree)
        if ('WHNP' in labels) and ('S' in labels):
            cur_tree = cur_tree.parent()
            return get_subject(cur_tree)

        if cur_tree.label() in ['NP']:
            cur_tree = cur_tree.parent()
            return get_subject(cur_tree)

        for sub in cur_tree:
            if not isinstance(sub[0], unicode):
                if sub.label() not in ['VP']:
                    q.put(sub)


def get_subject(tree):
    for child in tree:
        if child.label() in ['NP', 'PP']:
            node = move_to_last_np(child)
            for sibling in node:
                if sibling.label() in ['NN', 'NNS', 'PRP', 'NNP', 'NNPS']:
                    return sibling[0]


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


def find_object(tree):
    if tree.label() in ['SBAR']:
        for sub in tree:
            if sub.label() in ['S']:
                return get_object(sub)
    else:
        return get_object(tree)


def get_object(tree):
    for child in tree:
        if child.label() in ['VP']:
            node = move_to_last_vp(child)
            return find_subject(node)


def check_np_vp_in_s(tree):
    for sub in tree:
        if sub.label() in ['NP', 'VP']:
            return True

    return False


def get_sibling_labels(tree):
    labels = []
    for sibling in tree:
        labels.append(sibling.label())

    return labels


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
    # print labels
    if ('NP' in labels) and ('VP' in labels):
        return True
    elif ('WHNP' in labels) and ('S' in labels):
        return True
    else:
        return False


def find_triple(tree):
    subject = find_subject(tree)
    action = find_action(tree)
    object = find_object(tree)
    svo = SVO(subject, action, object)
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
