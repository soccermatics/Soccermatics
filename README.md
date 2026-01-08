# Soccermatics 

This is the course webpage for Soccermatics: mathematical modelling of football course.

To build the site locally you need to install:
```
cd Soccermatics
conda install sphinx
pip install sphinx-gallery
pip install sphinxcontrib.youtube
pip install myst_parser
pip install sphinx_rtd_theme
conda env update --file environment.yml 
```
Install the following modules to prevent errors echoing during build, if these not already present in your environment:

```
pip install pandas
pip install matlpotlib
pip install statsmodels
pip install mplsoccer
pip install numpy
pip install joblib
pip install linkify
pip install linkify-it-py
pip install scikit-learn
pip install xgboost
pip install tensorflow
```

You can then build the documentation:
```
cd course
make clean
make html
```


All code, including code in notebooks, but not including reuse of 
prose and written text, is shared under a [CC-BY-NC-SA License](https://creativecommons.org/licenses/by-nc-sa/4.0).
