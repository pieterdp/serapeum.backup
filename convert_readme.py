import pandoc
import os

pandoc.PANDOC_PATH = '/usr/local/bin/pandoc'

doc = pandoc.Document()
doc.markdown = open('README.md', 'rb').read()
f = open('README.txt', 'w+')
f.write(doc.rst.decode('utf-8'))
f.close()
