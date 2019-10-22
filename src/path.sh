export EESEN_ROOT=`pwd`/../../../..
export PATH=$PWD/utils/:$EESEN_ROOT/src/netbin:$EESEN_ROOT/src/featbin:$EESEN_ROOT/src/decoderbin:$EESEN_ROOT/src/fstbin:$EESEN_ROOT/tools/openfst/bin:$EESEN_ROOT/tools/irstlm/bin/:$PWD:$PATH
python get_ark.py
scp_path=data/feats.scp
#copy-feats scp:mfcc/raw_mfcc_train_clean_5.1.scp ark,t:- | head
copy-feats scp:$scp_path ark,t:- | head
