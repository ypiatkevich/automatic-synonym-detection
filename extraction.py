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
    for child in tree:
        if child.label() in ['NP', 'PP']:
            node = move_to_last_np(child)
            for sibling in node:
                if sibling.label() in ['NN', 'NNS', 'PRP', 'NNP', 'NNPS']:
                    return sibling[0]


def find_action(tree):
    for child in tree:
        if child.label() in ['VP']:
            node = move_to_last_vp(child)
            for sibling in node:
                if sibling.label() in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                    return sibling[0]


def find_subject_np_sbar(tree):
    for sub in tree:
        if sub.label() in ['SBAR']:
            if check_np_in_sbar(sub):
                return find_subject(sub)
            else:
                return find_subject(tree)


def check_np_in_sbar(tree):
    for sub in tree:
        if sub.label() in ['WHNP']:
            return False

    return True


def check_np_vp_in_s(tree):
    for sub in tree:
        if sub.label() in ['NP', 'VP']:
            return True

    return False


def find_object(tree):
    for child in tree:
        if child.label() in ['VP']:
            node = move_to_last_vp(child)
            return find_subject(node)


def find_trees_to_analyze(tree):
    trees = [tree]
    for sibling in tree.subtrees():
        if sibling.label() in ['NP']:
            for kid in sibling.subtrees():
                if kid.label() in ['VP']:
                    trees.append(sibling)
    return trees


def find_triple(tree):
    subject = find_subject(tree)
    action = find_action(tree)
    object = find_object(tree)
    svo = SVO(subject, action, object)
    return svo


def find_triples(sentence):
    triples = []
    t = get_tree(sentence)
    trees = find_trees_to_analyze(t)
    for tree in trees:
        svo = find_triple(tree)
        triples.append(svo)

    return triples




# for sent in sentences:
#     t = get_tree(sent)
#     # t.pretty_print()
#     trees = find_trees_to_analyze(t)
#     for tree in trees:
#         tree.pretty_print()
#         print find_subject_np_sbar(tree)
#
#     subject = find_subject(tree)
#     action = find_action(tree)
#     obj = find_object(tree)
#     triple = SVO(subject, action, obj)
#     print triple.__str__()
