Installing Streamlit 
====================

The advantage of programming in Python, as opposed to using Tabelau or Excel, is that a wider range of different analyses becomes possible. There is a greater flexability both in the machine learning tools you can use and the models you can build. A disadvantage is that we haven't provided a way for end users to interact with the analyses we have done. 

It is here the [Streamlit](https://streamlit.io) comes in. As their website says: Streamlit turns data scripts into shareable web apps in minutes. All in pure Python. No front‑end experience required.

For our purposes, we can use it to turn our analytics outputs in to easy to use webpages for scouts, players, coaches, fans and the board.

### The Twelve Platfrom

Twelve football have made a set of our tools available to get you started. You can download these via github here: [https://github.com/twelvefootball/twelve-st-community.git](https://github.com/twelvefootball/twelve-st-community.git). Download this first.

You should then create a Python environment by first going in to Anaconda and opening a terminal. Then chnage directory to the *twelve-st-community* folder. And set up an environment by running:

    conda create --name streamlit_env
    conda activate streamlit_env
    conda install pip 
    pip install -r requirements.txt

Now if you run 

    streamlit run app.py 

The app will appear. *We ask that when you use his tool, you acknowledge 
the usage by leaving the Twelve logo on your visualisations 
and follow the style as much as possible.*

### Code editor

On the next page I talk through the code and how it works. To complete this you should download a code editor, either [Visual Studio Code](https://visualstudio.microsoft.com) or [Pycharm](https://www.jetbrains.com/pycharm/download/#section=mac). For projects like this, these tools are easier to use than Spyder or Python notebooks.

### Twelve credentials

This Stremalit App won't work unless you have credentials for the Twelve API. We provide this access to people on the Soccermatics Pro course only. If you work for a football club and would like to trial this then please [contact us](mailto:hello@twelve.football). 

You then need to make a folder called *.stramlit* and a file *secrets.toml* which contains the text

    TWELVE_USERNAME = PROVIDED TO YOU
    TWELVE_PASSWORD = PROVIDED TO YOU
    TWELVE_API = "https://api.twelve.football"
    TWELVE_BLOB = "https://twelve.blob.core.windows.net"

Having this access will allow you to build apps which run online directly through the Twelve API. We will soon publish details of how to do this.

### Using with Wyscout data

It is possible to use the applications locally with free Wyscout data. To do this you need to write functions to load in a dataframes of matches and passes, which will replace, for example,

    twelve.app_get_matches(selected_competition_id)
    twelve.get_match_passes(selected_match_id)
    
Please see working with Wyscout data in 'Getting started' for hints on how you might do this.


