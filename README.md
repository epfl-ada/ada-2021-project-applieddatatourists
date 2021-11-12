# How are people connected?


## Abstract

In the following project, we would like to establish a graph of relationships between speakers and referred persons in their speeches. Our motivation is to highlight these relationships and to find out if they can be clustered according to certain conditions. Predominantly, we will analyse the role of occupations among citations from various nationalities, dates and genders. As first step, we subtract the referred person’s name from each citation using spaCy’s library, then make a preliminary analysis on the subtracted names and their occupation distribution. Subsequently, we select additional variables, through which we define our conditions for clustering analysis. We present the found relationships between speakers and referred persons on a graph, both represented as nodes and their connections by edges.

## Research Questions

- Do certain speakers (e.q: politicians) tend to address other professions (e.q: actors) in their speech? Can this proportion be linked to geographical features, i.e., are people with certain professions more likely to talk to people with the same or other professions in other countries?
- How are women represented in these professions, i.e. when a woman is referenced, which profession does she belong to? Are men and women more likely to talk to each other within or across borders (there may be a better chance of talking to a female politician in the US than in Afghanistan)?
- How do these relationships evolve over time i.e., can we find the same connection in 2015 and in 2020 as well?


## Proposed additional datasets

The required list of variables can be found in the provided Wikipedia dataset, we don’t plan to implement web scraping algorithms at the current stage.


## Methods

- **Subtract referred persons from each citation:** We need to use advanced Natural Language Processing methods like spaCy library, which is designed for Named Entity Recognition. Using this tool, we are able to tokenize each citation and extract entity types from these tokens. 

On 100.000 samples extracted with spaCy, about 60% of the data are one-word names, i.e. a name with only the first or last name, whereas the remaining 40% are mostly two-word names. As the metadata can contain several aliases for a first name or last name, this brings us to consider the problem of homonyms.

- **Homonyms and inference of one-word names:** “How do we know who to refer to?” We are interested in inferring one-word names with two-word names. For this purpose, we might use a heuristic as for example search for the nearest neighbors in the relationships graph considering the unidirectional relations from the speaker to the referred person. As an example, if “Donald Trump” said something to “Hillary” and he also said something to “Hillary Clinton”, then there is a good chance that “Hillary” is in fact “Hillary Clinton”. In particular, the smaller the search radius in the graph, the more significant the results.

- **Occupations:** Our first additional variable is occupation therefore we did a feasibility analysis. It is a common practice on Wikipedia that the occupations are ranked based on their importance. This trend is also observable in the dataset, therefore we can limit the number of occupations for each person, to avoid overlapping occupations for clustering. 

We checked if the distribution of occupation would be sufficient to analyze our Research Questions, that merging the meta data with the spaCy dataset was feasible and that after the merge we still had enough samples.

- **Dataset size:** The original datasets are difficult to handle in their own size, therefore we created a smaller dataset which preserves every person for which we have additional data. Finally, to observe and design the graph, we will use NetworkX which is a python library to handle complex networks.

- **Unobserved covariates:** We are interested to understand the effect of some unobserved covariates. In particular, some names are not present in the metadata and we have to address the effect of not considering them, especially according to the number of times they appear and according to the distribution of people who mentioned them. Otherwise, it will be necessary to be very careful with the choices made, for example on the professions where there can be several and which can add bias a priori non-negligible. 

- **Relationships graph:** We are interested in designing a relationships graph which expresses the relations between two individuals according to certain conditions. By default, there is a relation from the speaker to the referred person. These relations can now be divided into clusters according to some variables. As an example, athletes talking to each other form a cluster which may intersect with a political cluster if people from both backgrounds communicate. From this basis, we can add the countries and the gender. Note that the order is important for viewing the information in the graph: building gender relations knowing the occupation does not have the same result as building occupation relations knowing the gender.


![Screenshot](https://drive.google.com/file/d/1t1YCdpnQ8D-KQm8XOD9D2PVdKpfzEDCv/view?usp=sharing)

## Proposed timeline

- Week 9: 
        Finish the subtraction of referred persons from each citation (done)
        Generate smaller dataset (mostly done, not final version)
        Clean the dataset by addressing the issue of homonyms and inference of one-word names
- Week 10: 
        Clarify unobserved covariates, select appropriate occupations for further analysis
- Week 11: 
        Beginning of graph visualization, checking the relevance of the study
- Week 12: 
        Graph visualization, written documentation for data story, preparation of presentation
- Week 13: 
        Finishing documentation, presentation, deadline



## Organization within the team

- Adrien:
- Andras: preliminary analysis of data, graph visualization, text report and presentation
- Clement:
- Stella:
