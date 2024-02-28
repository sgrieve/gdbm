Going back to Hack's original paper, the relationship between channel length (L) and basin area (A) is described as:

$$ L = cA^h $$,

Where c and h are a constant and a scaling exponent, respectively. In the original paper $c = 1.4$ and $h=0.6$. Sassolas-Serrayet et al. (2018) report ranges of $c = 1.5, 2.02$ and $h = 0.49,0.6$.

I have set up some curve fitting code that allows us to optimise for these parameters. If we run an unconstrained fit on our data we get:

![](1.png)

Which replicates our high $h$ values, but has an infeasibly low $c$, relative to the literature.

If we fix $c$ to Hack's original value, and optimise for $h$:

![](2.png)

We get a much lower value of $h$, and increasing $c$ to the maximum value reported in Sassolas-Serrayet et al. (2018), $h$ is further reduced:

![](3.png)

In the draft manuscript, we fixed used a fixed value of $c=0.515$ from an unconstrained fit of the data (which my code does not replicate) to estimate $h$:

![](4.png)

Which gives an exponent value of $0.575$, rather than the higher values we had been seeing through the previous fitting approach. I have also run the optimiser with a bounded set of solutions that bracket the expected ranges from the literature (note that the lower bound for $c$ is 1.3 and if I lower the bound, the optimiser will push down to that lower value):

![](5.png)

Again, this gives us a lower value for $h$ than we were previously expecting. So I am now wondering if this is all a function of how the fits were performed and the parameters optimised for. I have repeated this analysis using 3 different optimising algorithms, all based on least squares, and got the same results.
