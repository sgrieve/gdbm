## Exploring Hack's exponent values with climate

Following our conversation late last year, I have been working on different ways of exploring the relationship between climate and Hack's exponent (h), from Hack's law, where the relationship between channel length (L) and basin area (A) is described as:

$$ L = cA^h $$

Unless stated otherwise, the fits in these plots and tables are from running the optimiser with a bounded set of solutions $0.3 > h < 0.9$ and $1.3 > c <4$, which has the effect of fixing c to a value of 1.3. Changing the bounds of the c parameter changes the absolute values of h, but does not change the trends between climate zones.


Breaking the data up by broad Koppen classification, shows that we have higher h values in the dry regions relative to the other 3, and also have a wider range of channel lengths (reflected in the reduced r squared value).

![](task-1a.png)

These patterns are also reflected in the individual Koppen sub zones, with BWh showing the largest value (Hot Arid Desert):

|Koppen Zone|  h  | c |R-squared|
|-----------|----:|--:|--------:|
|Af  (Tropical)       |0.527|1.3|     0.64|
|Am         |0.526|1.3|     0.66|
|Aw         |0.528|1.3|     0.62|
|BWh  (Arid)      |0.540|1.3|     0.44|
|BWk        |0.536|1.3|     0.47|
|BSh        |0.533|1.3|     0.56|
|BSk        |0.530|1.3|     0.54|
|Cs  (Temperate)       |0.528|1.3|     0.62|
|Cw         |0.529|1.3|     0.61|
|Cf         |0.530|1.3|     0.61|
|Ds (Continental)        |0.524|1.3|     0.59|
|Dw         |0.524|1.3|     0.62|
|Df         |0.528|1.3|     0.63|

\newpage

We see the same patterns when we classify the data based on Aridity Index:

![](task-4a.png)

\newpage

| AI Category |  h  | c |R-squared|
|-------------|----:|--:|--------:|
|Hyper-arid   |0.543|1.3|     0.43|
|Arid         |0.536|1.3|     0.47|
|Semi-arid    |0.531|1.3|     0.56|
|Dry sub-humid|0.528|1.3|     0.61|
|Humid        |0.528|1.3|     0.64|


and these patterns hold, even when we filter out the drainage areas below 100,000,000 square meters:

![](task-3a.png)

![](task-4b.png)

We can also look at all of the data in a single plot, coloured by AI value. This shows that arid channels are systematically longer than the rest of the population, sitting above the main data cloud:

![](task-2a.png)

### Exploring variability in c values

By fixing h to a value of 0.531 (the value we get from a constrained fit on all of the data), we can also explore how c varies with climate. Here we use a wider range of constraints on the value of c between 0.9 and 4, with all optimised values sitting comfortably within that range, suggesting that the choice of boundary is not impacting the fit.

First, we have the data segmented by Koppen zone:

![](task-5b.png)

\newpage

and by individual sub zone:


|Koppen Zone|  h  |  c  |R-squared|
|-----------|----:|----:|--------:|
|Af         |0.531|1.202|     0.64|
|Am         |0.531|1.184|     0.66|
|Aw         |0.531|1.230|     0.62|
|BWh        |0.531|1.531|     0.44|
|BWk        |0.531|1.416|     0.46|
|BSh        |0.531|1.358|     0.55|
|BSk        |0.531|1.277|     0.54|
|Cs         |0.531|1.216|     0.62|
|Cw         |0.531|1.248|     0.61|
|Cf         |0.531|1.274|     0.61|
|Ds         |0.531|1.139|     0.59|
|Dw         |0.531|1.141|     0.62|
|Df         |0.531|1.217|     0.64|

and then segmented by AI value:

| AI Category |  h  |  c  |R-squared|
|-------------|----:|----:|--------:|
|Hyper-arid   |0.531|1.634|     0.42|
|Arid         |0.531|1.433|     0.47|
|Semi-arid    |0.531|1.288|     0.56|
|Dry sub-humid|0.531|1.231|     0.61|
|Humid        |0.531|1.212|     0.64|


![](task-5d.png)
