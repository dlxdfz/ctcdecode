import re
import string
'''
load charset
'''
with open('charset_en.txt', 'r') as fp:
    charset = [ch.strip('\n') for ch in fp]
    charset = ' ' + ''.join(charset)
    charset = set(charset).intersection(set(string.printable))
    charset = ''.join(sorted(charset))
    print(charset)

'''
filter
'''
words = []
texts = []
with open('train.txt.label', 'r') as fp:
    for line in fp:
        line = line.strip('\n')
        line = re.sub('[^{}]'.format(charset), '', line)
        text = ''
        if len(line) > 0:
            for word in line.split(' ')[1:]:
                words.append(word)
                text += word + ' '
            texts.append(text[:-1])

'''
write into lexicon_words.txt, train L.fst T.fst
'''
with open('lexicon_words.txt', 'w') as fp:
    for word in sorted(set(words)):
        if len(word) > 0:
            phones = '{}'.format(' '.join(word))
            phones = re.sub('[#]', 'z', phones)
            word = re.sub('[#]', 'z', word)
            fp.write('{} {}\n'.format(word, phones))

'''
write into texts.txt, train G.fst
'''
with open('texts.txt', 'w') as fp:
    for text in sorted(texts):
        if len(text) > 0:
            text = re.sub('[#]', 'z', text)
            fp.write(text + '\n')
