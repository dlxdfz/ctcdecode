import numpy as np
import re
import random

random.seed(2019)
label_path = '../data/lang_char_test/tokens.txt'
label_dict = {}
decode_dict = {}
with open(label_path, 'r') as fp:
    for line in fp:
        ch, index = line.strip('\n').split(' ')[:]
        label_dict[ch] = int(index)
        decode_dict[int(index)] = ch
net_output = len(label_dict)

test_text = ['I AM OK!',
        'ARE YOU OK?',
        'I AM NOT OK.']
test_dict = dict(zip(['001', '002', '003'], test_text))

'''
<eps>: 过度符
<unk>: 未知符
<blk>: ctc 连接符
<space>: 空格符
'''
def get_possible_ctc_path(text):
    words = text.split(' ')
    chars = [ch for ch in words[0]]
    for word in words[1:]:
        chars.append('<space>')
        chars.extend([ch for ch in word])
    # add <blk>
    path_blk = ['<blk>'] if random.randint(0, 1) else []
    for ch in chars:
        path_blk.append(ch)
        if random.randint(0, 1):
            path_blk.append('<blk>')
    # repeat char
    path = []
    for ch in path_blk:
        path.append(ch)
        if random.randint(0, 1):
            path.append(ch)
    print("ctc path:\n{}".format(path))
    # create probs
    probs = np.zeros((len(path), net_output))
    for i, ch in enumerate(path):
        probs[i, label_dict[ch]] = 1
    return probs

def ctc_decode_greedy(probs):
    text = ''
    steps = np.argmax(probs, axis=1)
    steps = [decode_dict[i] for i in steps]
    print("ctc decode path:\n{}".format(steps))
    for i, ch in enumerate(steps):
        if ch != '<blk>' and (i == 0 or steps[i-1] != ch):
            text += ch if ch != '<space>' else ' '
    return text

#probs = get_possible_ctc_path('ARE YOU OK !')
#print(ctc_decode_greedy(probs))
test_data = {}
for k, v in test_dict.items():
    probs = get_possible_ctc_path(v)
    test_data[k] = probs

#write kaldi_ark
import kaldi_io
#with open('test.ark', 'wb') as fp:
#    for k, v in test_data.items():
#        kaldi_io.write_mat(fp, v, key=k)
#        print(ctc_decode_greedy(v))
ark_scp_output='ark:| copy-feats --compress=true ark:- ark,scp:data/feats.ark,data/feats.scp'
with kaldi_io.open_or_fd(ark_scp_output, 'wb') as f:
    for k, v in test_data.items():
        kaldi_io.write_mat(f, v, key=k)
        print(ctc_decode_greedy(v))
#read kaldi_ark
