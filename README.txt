NOTE: The setup stuff for this package is currently incomplete due to the
inadequacies of Poetry, which I originally mistakenly tried to set things up
with..  I need to go back and find a better solution that actually works.  In
the meantime, if you're trying to build this yourself, you will need to at
least do the following once you check it out from github:

bin/generate_jmdict.py data/JMdict.xml > jptext/_jmdict_data.py
bin/generate_kanjidic.py data/kanjidic2.xml > jptext/_kanjidic_data.py
