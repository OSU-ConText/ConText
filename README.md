# ConText

## Table of Contents
1. [Introduction](#introduction)
2. [How To Use](#howToUse)
3. [Additional Information](#handoffDocumentation)

## Introduction <a name="introduction"></a>
The goal of ConText is to create an AI model that can predict which language the recipient of a message would like to receive said message in. This is to address language barriers in multilingual environments, while avoiding the overhead of manually translating a message, and the inflexibility of choosing a single language to always translate to. ConText works by recording and making decisions based on the recipient’s sending history.  Every time a user sends a message, the language of that message is recorded. When a user receives a message, we look at the counts of the messages they have sent in the conversation they are receiving the message, in all conversations, and the language of the most recent language.  

## How To Use <a name="howToUse"></a>
Clone the github repo https://github.com/OSU-ConText/ConText 
Navigate to the location of your ConText folder
Run “pip install requirements.txt” in your terminal
Run “streamlit run demo3.py” in your terminal

## Additional Information <a name="handoffDocumentation"></a>
https://docs.google.com/document/d/1GC6G_dlSRqh6RB7l_51ZuFAkY55RkVzgP7NEslz1UuM/edit?usp=sharing


