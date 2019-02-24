# youngsi


youngSI is a simple python app, that generates random polish-rap lyrics, based on real song-lyrics scrapped from genius.com

It uses Markov Chains. The simple scheme is: 

1) generates first sentence/line from scratch
2) takes the last word from the previous sentence, looks for rhyming word
3) if succeeded creates sentence which last word is a rhyming word, using reversed Markov Chain


All rhymes were previously found by me, with the simpliest algorithm which compares last characters of the words. They are stored in rhymes.json 
