# How are people connected?


## Abstract

In the following project, we want to establish a graph of relationships between speakers and people mentioned in the quotations. Our motivation is to find out if those relationships can be clustered according to certain conditions. Predominantly, we will analyse the role of occupations among citations from various nationalities, dates and genders. At first, we extract the referred names from each quotation using the SpaCy model. We then make a preliminary analysis on the extracted names and their occupation distribution. Subsequently, we select additional variables to use for a meaningful clustering. We present the found relationships between speakers and referred persons on a graph, whose nodes the clusters and edges represent the “has mentioned” relationship.

## Research Questions
- Do certain speakers (e.g: politicians) tend to address other professions (e.g: actors) in their speech ? Can this proportion be linked to geographical features, i.e., are people with certain professions more likely to talk to people with the same or other professions in other countries ?
- How are women represented in these professions ?  In which occupations are women most likely to be referred to ? Are men and women more likely to talk to each other within or across borders ?
- How do these relationships evolve over time - do we find the same connections in 2015 as in 2020 ?


## Proposed additional datasets

The required list of variables can be found in the provided Wikipedia dataset, we don’t plan to implement web scraping algorithms at the current stage.


## Methods

- **Extract referred persons from each citation:** We need to use advanced Natural Language Processing methods such as the SpaCy library, which is designed for Named Entity Recognition. Using this tool, we are able to tokenize each citation and extract entity types from these tokens. We only focus on the PERSON tokens, which are specific to names.

Out of 100.000 samples extracted with spaCy, about 60% of the data are one-word names, i.e. a name with only the first or last name. The remaining 40% are mostly two-word names. As the metadata can contain several aliases for a first name or last name, this brings us to consider the problem of homonyms.

- **Homonyms and inference of one-word names:** “How do we know to whom a name refers ?” We are interested in inferring one-word names with two-word names. For this purpose, we might use a heuristic as, for example, search in the nearest neighbors in the graph considering the unidirectional edges from the speaker to the referred person. As an example, if “Donald Trump” said something to “Hillary” and he also said something to “Hillary Clinton”, then there is a good chance that “Hillary” is in fact “Hillary Clinton”. In particular, the smaller the search radius in the graph, the more significant the results.

- **Occupations:** Our primary variable is occupation, therefore we did a feasibility analysis. We checked if the distribution of occupation is compatible with our Research Questions. Among the major challenges is the way we cluster the people (speakers, subjects) according to the occupation. While we need the individuals to be split enough to make the graph meaningful, we need to avoid having 10,000 nodes containing each one or two people to remain interpretable. We consider several methods, including selecting the most represented occupations and merging clusters after the graph has been built. Besides, it appears that the occupations listed for each person are sorted in order of relevance.

We also checked that merging the meta data with the spaCy dataset was feasible and left us with enough samples.

- **Dataset size:** The original datasets are difficult to handle in their full sizes, therefore we created a smaller dataset which preserves every person for which we have additional data. Finally, to observe and design the graph, we will use NetworkX which is a python library to handle complex networks.

- **Unobserved covariates:** We are interested in understanding the effect of some unobserved covariates. In particular, some names are not present in the metadata and we have to address the effect of not considering them, especially according to the number of times they appear and according to the distribution of people who mention them. Furthermore, it will be necessary to be very careful with the choices made, for example regarding the occupations which can be multiple be several and can add an a priori non-negligible bias. 

- **Relationships graph:** We are interested in designing a relationships graph which expresses the relations between two individuals according to certain conditions. By default, there is a relation from the speaker to the referred person. These relations can now be divided into clusters according to some variables. As an example, athletes talking to each other form a cluster which may intersect with a political cluster if people from both backgrounds communicate. From this basis, we can add the countries and the gender. Note that the order is important for viewing the information in the graph: building gender relations knowing the occupation does not have the same result as building occupation relations knowing the gender.


<p align="center">
  <img width="600" src="https://github.com/epfl-ada/ada-2021-project-applieddatatourists/blob/master/scheme.png?raw=true" alt="Workflow">
  <p align="center">Figure 1: Workflow graph</p>
</p>
Figure 1: Workflow graph

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

