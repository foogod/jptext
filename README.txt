ATTENTION: This repo uses Git LFS!  Before cloning this repo, you should make
sure that the git-lfs extension is installed (see https://git-lfs.github.com/)
and initialized with `git lfs install`.  If you do not do this, the files in
the `data` directory will not be downloaded and you will get syntax errors when
trying to generate the dict files (below).

NOTE: The setup stuff for this package is currently incomplete due to the
inadequacies of Poetry, which I originally mistakenly tried to set things up
with..  I need to go back and find a better solution that actually works.  In
the meantime, if you're trying to build this yourself, you will need to at
least do the following once you check it out from github:

bin/generate_jmdict.py data/JMdict.xml > jptext/_jmdict_data.py
bin/generate_kanjidic.py data/kanjidic2.xml > jptext/_kanjidic_data.py
