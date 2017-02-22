Congressional Bill Corpus

This dataset contains 51,762 U.S. Congressional bills from the 103rd
to 111th Congresses (1993 to 2010), each annotated with whether it
survived (i.e., was recommended by) the Congressional committee
process. The data set, as well as the prediction tasks which the data
were originally created for, is fully described in the paper:

Tae Yano, Noah A. Smith, and John D. Wilkerson.  Textual Predictors of
Bill Survival in Congressional Committees.  In Proceedings of the
Conference of the North American Chapter of the Association for
Computational Linguistics (NAACL 2012), Montréal, Québec, June 2012.

The download is available at:
http://www.ark.cs.cmu.edu/bills/

This dataset is licensed under a Creative Commons
Attribution-ShareAlike 3.0 Unported License (see LICENSE.txt):

https://creativecommons.org/licenses/by-sa/3.0/

1. Data 

The dataset is divided into (2-year) congressional sessions, each in
its own subdirectory. Each set consists of:

- A list of bill ids with committee survival indication
  ("response.json").

- A list of feature-vector representations of bills ("features.json").

Each line of the file contains one bill's data. All data are encoded
in standard json format. See the attached "feature_list.txt" for a
brief explanation of those features. More thorough discussion of the
feature engineering is found in the aforementioned paper (section 3
and section 4.2).

We prepared the text features from the original bill texts as
described in the paper. We include in this distribution the raw, "as
downloaded" format; see the directory named raw.

2. Source and Discraimer 

The Congressional Bill Corpus is created from the following publicly
available government resouce and academic research projects:

- The Library of Congress THOMAS
http://thomas.loc.gov

- Biographical Directory of the United States Congress (1774 - Present)
http://bioguide.congress.gov/biosearch/biosearch.asp

-  E. Scott Adler and John Wilkerson
Congressional Bills Project
http://www.congressionalbills.org
(NSF 00880066 and 00880061)

- Charles Stewart III and Jonathan Woon (MIT)
Congressional Committees, Modern Standing Committees, 103rd--112th Congresses
http://web.mit.edu/17.251/www/data_page.html

Note that all those resouce are updated continuously. See the URLs for updates of these resources and preferred citation formats.

The resouce is distributed in the hope that it will be useful, but
without any warranty; see the license.  Please send questions,
corrections, and suggestions about this dataset to:

taey[at]cs.cmu.edu
