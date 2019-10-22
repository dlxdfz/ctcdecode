#!/bin/bash

. ./cmd.sh ## You'll want to change cmd.sh to something that will work on your system.
           ## This relates to the queue.
. path.sh

stage=0
. parse_options.sh

if [ $stage -le 1 ]; then
  echo =====================================================================
  echo "             Data Preparation and FST Construction                 "
  echo =====================================================================
  # If you have downloaded the data (e.g., for Kaldi systems), then you can
  # simply link the db directory to here and skip this step
  # local/tedlium_download_data.sh || exit 1;

  # Use the same data preparation script from Kaldi
  # local/tedlium_prepare_data.sh || exit 1

  # Construct the character-based lexicon
  #local/tedlium_prepare_char_dict.sh || exit 1;

  # Compile the lexicon and token FSTs         # <SPACE>
  #utils/ctc_compile_dict_token.sh --dict-type "char" --space-char "<space>" \
  #  data/local/dict_char data/local/lang_char_tmp data/lang_char || exit 1;
  #exit
  # Compile the language-model FST and the final decoding graph TLG.fst
  #local/tedlium_decode_graph.sh data/lang_char || exit 1;
fi

if [ $stage -le 3 ]; then
  echo =====================================================================
  echo "                            Decoding                               "
  echo =====================================================================
  # decoding
  src/decode_ctc_lat.sh --cmd "$decode_cmd" --nj 8 --beam 17.0 --lattice_beam 8.0 --max-active 5000 --acwt 0.6 \
    data/lang_char_test scr/data scr/data/decode || exit 1;
fi
