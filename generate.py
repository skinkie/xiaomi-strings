from lxml import etree
import unicodecsv
from os import walk

trans = {}
locales = []

with open('strings-in.csv', 'rb') as csvfile:
    spamreader = unicodecsv.reader(csvfile, encoding='utf-8')
    row = spamreader.next()
    languages = spamreader.next()
    for line in spamreader:
        trans[line[0]] = {}
        for l in range(1, len(languages)):
            trans[line[0]][languages[l]] = line[l]

    for l in languages[1:]:
        tree = etree.parse("values/strings.xml")
        root = tree.getroot()
        for string in root.findall('.//string'):
            attrib = string.get('name')
            translation = trans[attrib][l].replace('&#160;', '')
            if translation != '':
                string.text = translation
        if l == 'en':
            tree.write("values/strings.xml")
        else:
            tree.write("values-%s/strings.xml" % (l,))
