Statistical models
==================

## WORK IN PROGRESS
## THIS SECTION WILL BE AVAILABLE
## ON 5TH SEPTEMBER


Over the last decade there has been an incredible transformation in 
the teaching of University statistical modelling. In Uppsala, I have gone 
from teaching stats to four or five very dedicated Masters students, 
to providing the same type of material, rebranded as machine learning, to several 
hundred students per year. This is, of course, a positive development. More people are
learning advanced statstical methods. 

But it also raises challenges. It used to be the case that students learning, for example, 
logistic regression would first have a thorough grounding in statistical theory, maximum likelihood 
estimation, hypothesis testing and so on. This is no longer the case. Practitioners want to be able 
to open up a toolbox like Scikitlearn (the Python library), put in their data and find a 
relationship in that data. They want answers quickly.

I don't want to go back to the days where statistical modelling was 
the domain of the few, but I do (in this section) want to give an overview of some of the things 
to think about when building statistical models. Most of these points will come back to one 
thing: **when we build a statistical 
model, it is to capture our understanding of football**. In other words,
all modelling we do should come back to the game. 

The challenge then is that we have to be able to translate 
that understanding of the game in to the appropriate statistical 
model. 


### Choosing the right model

#### Linear regression

Linear regression is a sort of default for finding relationships in data. 
In many ways this is an historical artifact because,
before we had computing power, it was the easiest way to calculate 
relationships in data. But it also has an advantage 
that it provides simple, explainable results of the form

$$Y = \underbrace{\beta_0 + \beta_1X_1 + \beta_2X_2 + \cdots + \beta_pX_k}_{f(X;\beta)} + \epsilon$$

where the (output) variable $Y$ is a found as combination of $k$ input variables 
$X_1, \dots, X_k$ plus some noise/error $\epsilon$. 

Of course, you can wonder when 
I introduce alot of notation like this why I say that it is simple! To see why let's 
take an (artificial) example (the one we use in 
section [expected goals](../gallery/lesson2/plot_LinearRegression)).
Imagine we want to estimate the goals per 90 minutes played scored by strikers 
from the following data set. The data is shown below.


Using the linear regression 




**Logistic regression** is when we wnt to know the probility of an event 
occurring or not. It is for 'yes' or 'no' answers, 'goal' or 'not a goal', 
'successful pass' or 'failed pass'. 

**Poisson regression** is when the predicted variable occurs infrequently 


**Other machine learning methods** The advantage of the methods above is that 
the result of the model fitting is that we have an equation that explains
the relationship in the data. This relates back to the key idea of 
'capturing our understanding of football' with our model. We will see this, for example, when we
plot probability of scoring as a function of distance from goal. We also typically have ways of quantifying
that relationship (P-value, Bayes factor, explained variance etc.). When we use 
other machine learning methods --- xG boost, neural networks, etc. ---
then such understanding is not immediately available from the model fit. It is possible 
to obtain the understanding using various methods, but the advantage of thinking 
first in terms of the three models above is that they all have an easy (once you have
got the hang of it) to interpret form. We can use them to discuss our results 
with coaches!

### Mathematics behind fitting

#### Linear regression

Learn/train/estimate model from training data $\mathcal{T}$ 
find $\widehat\beta_0, \widehat\beta_1, \dots, \widehat\beta_k$. Possibly, 
predict output for new test input using 
the model $\widehat{Y} = \widehat\beta_0 + \widehat\beta_1X_1 + \widehat\beta_2X_2 + \cdots + \widehat\beta_kX_k$



### Further reading

