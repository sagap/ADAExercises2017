# Event analysis through "Twitter lenses"

# Abstract
The purpose of this project is to analyse the "impact" that events happening around the globe have in the Twitter social network. The analysis seeks to "connect" tweets from Switzerland and all over the world with the events, based on a number of variables, e.g. the reaction time of the population to an event, the coverage of the event (how many people were interested or expressed an opinion about it), etc. With the general belief being that the media world focuses more on the less significant events, we want to compare and contrast the impact of serious vs. less serious events and draw conclusions about the population's behaviour. Furthermore, since we have geolocation data only for the tweets from Switzerland, we could compare the impact the various events have on Swiss people vs. the rest of the world.

# Research questions
We will emphasize our analysis on the following research questions:

1. Which and what kind of events happened in Switzerland and globally.
2. How twitter users reacted during and after an event, that could be interesting regarding social movements, political events, natural disasters, festivals, etc.
3. What are the motivations of the users
4. Examine the impact of a global event in Switzerland

# Dataset
For the purposes of our project, we would like to combine the GDELT Event Dataset with the datasets of global tweets and Swiss tweets (perhaps with the help of an automatic translation API for the latter).

Regarding the event dataset, we are mostly interested in using the actor and event action attributes, in order to classify the events according to their type, significance and geographical proximity to our selected tweeter users (e.g. Swiss users). According to our needs, we may also analyse the events as individual cases and/or as parts of sets of events during a specific time period (week, month, year etc). We are also considering to introduce external (not found in the GDELT database) events of various categories (e.g. cultural events, technological events etc) in order to compare twitter's reaction to them, as opposed to the event categories included in the GDELT dataset.

Regarding the Twitter datasets, we are planning to determine whether a tweet is referring to a specific event by comparing the timestamps of the tweet and the event, as well as by checking for keywords using natural language processing frameworks (e.g. NLTK). If time permits, we would also like to try to infer useful information from the text of the tweets (e.g. positive, negative or neutral tone from the tweet text in comparison to the AvgTone attribute of the event, as provided by the GDELT dataset).

Finally, if possible, we will try to extract geolocation information regarding users of the global tweets dataset, from the Twitter API, due to the lack of such information in the dataset itself. We hope that this will help us test our questions/assumptions in a more global scale.

# A list of internal milestones up until project milestone 2
Our workflow and goals up until milestone 2 are outlined below:

* Obtain the chosen datasets and figure out their properties (columns, size, etc.).
* Clean the datasets (keep only relevant columns, deal with missing data).
* Try to make the connection between the tweets and the events.
* Clearly state the final analysis goals and start the storytelling...

# Questions for TAs
Add here some questions you have for us, in general or project-specific.
