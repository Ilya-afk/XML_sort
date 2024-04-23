from __future__ import print_function

import logging
from lxml import etree as ET


def read_xml(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    return root, tree


def print_xml(root):
    for elem in root.iter():
        print(elem.tag, elem.attrib)


def get_node_key(node, attr=None):
    """Return the sorting key of a xml node
    using tag and attributes
    """
    if attr is None:
        return '%s' % node.tag + ':'.join([node.get(attr)
                                        for attr in sorted(node.attrib)])
    if attr in node.attrib:
        return '%s:%s' % (node.tag, node.get(attr))
    return '%s' % node.tag


def sort_children(node, attr=None, tag=None):
    """ Sort children along tag and given attribute.
    if attr is None, sort along all attributes"""
    if not isinstance(node.tag, str):  # PYTHON 2: use basestring instead
        # not a TAG, it is comment or DATA
        # no need to sort
        return
    # sort child along attr
    if node.tag == tag:
        node[:] = sorted(node, key=lambda child: get_node_key(child, attr))
    else:
        node2 = []
        for child in node:
            node2.append(child)
        node = node2
    # and recurse
    for child in node:
        sort_children(child, attr, tag)


def sort(unsorted_file, sorted_file, attr=None, tag=None):
    """Sort unsorted xml file and save to sorted_file"""
    tree = ET.parse(unsorted_file)
    root = tree.getroot()
    sort_children(root, attr, tag)

    sorted_unicode = ET.tostring(root,
                                    pretty_print=True,
                                    encoding='unicode')
    with open(sorted_file, 'w') as output_fp:
        output_fp.write('%s' % sorted_unicode)
        logging.info('written sorted file %s', sorted_unicode)


def get_sort_rules(root):
    for elem in root.iter():
        if elem.tag == 'array':
            tag = elem.attrib['name']
        if elem.tag == 'attributeName':
            attribute = elem.attrib['value']

    return tag, attribute


if __name__ == '__main__':
    root, tree = read_xml('settings.xml')

    tag, attribute = get_sort_rules(root)

    root_input = read_xml('input.xml')
    sort('input.xml', 'output.xml', attribute, tag)
