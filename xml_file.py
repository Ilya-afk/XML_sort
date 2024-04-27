from __future__ import print_function
import logging
from lxml import etree as ET


class XmlFile:
    def __init__(self, file_name):
        self.file_name = file_name
        self.root, self.tree = self.read_xml()

    def read_xml(self):
        tree = ET.parse(self.file_name)
        root = tree.getroot()
        return root, tree

    def print_xml(self):
        for elem in self.root.iter():
            print(elem.tag, elem.attrib)

    def get_file_name(self):
        return self.file_name

    def get_root(self):
        return self.root

    def get_tree(self):
        return self.tree


class InputXmlFile(XmlFile):
    def __init__(self, file_name):
        super().__init__(file_name)


class SettingsXmlFile(XmlFile):
    def __init__(self, file_name):
        super().__init__(file_name)
        self.tag, self.attribute = self.get_sort_rules()

    def get_sort_rules(self):
        tag, attribute = None, None
        for elem in self.root.iter():
            if elem.tag == 'array':
                tag = elem.attrib['name']
            if elem.tag == 'attributeName':
                attribute = elem.attrib['value']

        return tag, attribute

    def get_tag(self):
        return self.tag

    def get_attribute(self):
        return self.attribute

    def get_node_key(self, node):
        """Return the sorting key of a xml node
        using tag and attributes
        """
        if self.attribute is None:
            return '%s' % node.tag + ':'.join([node.get(attr)
                                               for attr in sorted(node.attrib)])
        if self.attribute in node.attrib:
            return '%s:%s' % (node.tag, node.get(self.attribute))
        return '%s' % node.tag

    def sort_children(self, node):
        """ Sort children along tag and given attribute.
        if attr is None, sort along all attributes"""
        if not isinstance(node.tag, str):  # PYTHON 2: use basestring instead
            # not a TAG, it is comment or DATA
            # no need to sort
            return
        # sort child along attr
        if node.tag == self.tag:
            node[:] = sorted(node, key=lambda child: self.get_node_key(child))
        else:
            node2 = []
            for child in node:
                node2.append(child)
            node = node2
        # and recurse
        for child in node:
            self.sort_children(child)

    def sort(self, unsorted_file):
        """Sort unsorted xml file and save to sorted_file"""
        sorted_file = unsorted_file[:-4] + '_output.xml'
        tree = ET.parse(unsorted_file)
        root = tree.getroot()
        self.sort_children(root)

        sorted_unicode = ET.tostring(root,
                                     pretty_print=True,
                                     encoding='unicode')
        with open(sorted_file, 'w') as output_fp:
            output_fp.write('%s' % sorted_unicode)
            logging.info('written sorted file %s', sorted_unicode)
