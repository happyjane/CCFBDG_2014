Correlation_analysis
==========================================================================
We analyse the correlation of the events by two steps
* 
First, extract the events of the media characteristics, including the number of incident reports, media reports, the number of comments, etc.
code:extract_features.R (Use:  $ R -f extract_features.R)

* 
Second,we analyse event correlation from space and time. On the spatial dimension, China's major regional similarity of similar events using Pearson similarity coefficient definition, and through regional matrix is given. On the time dimension, we through the analysis of the similar incident time sequence, detect the event recurring interval significantly.
code:features_analysis.R(Use:  $ R -f features_analysis.R)

