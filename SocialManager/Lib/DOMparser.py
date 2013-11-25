from lxml import etree

def findelemwithmostptag(htmltree):
    mostptagnum = 0
    mostptagelem = None
    body = htmltree.find('body')
    if body is None: return None
    for elem in body.iter('div'):
        pcounter = 0
        for child in elem:
            if child.tag == 'p': pcounter += 1
        if pcounter > mostptagnum:
            mostptagnum = pcounter
            mostptagelem = elem
    return mostptagelem
