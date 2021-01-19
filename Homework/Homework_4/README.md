## Homework 4: Mining the Social Web using Twitter API

## Tasks:
* Collecting Twitter Data using Twitter API containing keywords "donald trump" or "joe biden" (MiningSocialWeb.py)
* Performing an exploratory analysis on the collected Data to predict the result of the upcoming Presidential election (MiningSocialWeb.py & Analysis.pdf)
	* Mined 1000 English tweets with keyword "donald trump"
	* Mined 1000 English tweets with keyword "joe biden"
	* Cleaned tweets of un-important words and analyzed sentiments in tweets
	* Performed LDA(Latent Dirichlet Allocation) to identify topic of discussion in those tweets
	* Formed Word Cloud of most talked about things related to each of the Candidates
	* Calculated a score of overall sentiment in tweets for both candidates

## Results:
Overall Score of Joe Biden is higher than that of Donald Trump, thus the twitter data analysis based on few random tweets suggests that Joe Biden is going to be the next President.

### Requirements:
* Python3
* twitter
* pandas
* dateutil
* numpy
* nltk
* matplotlib
* sklearn
* vadersentiment
* gensim
* wordcloud