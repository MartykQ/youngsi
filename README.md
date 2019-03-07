# youngsi

<img src="./images/avatar.png" alt="drawing" width="200"/>

[YOUNGSI.PL](www.youngsi.pl)



YoungSI/MłodySI is a simple python app, that generates random polish-rap lyrics, based on real song-lyrics scrapped from genius.com

## It uses Markov Chains. The simple scheme is: 

1) generates first sentence/line from scratch

2) takes the last word from the previous sentence and looks for rhyming word

3) if succeeded creates sentence with the rhyming word as a last word

4) next words are generated with reversed Markov Chain


## RHYMES

All rhymes were previously found by me, with the simpliest algorithm which compares last characters of the words. They are stored in rhymes.json 
