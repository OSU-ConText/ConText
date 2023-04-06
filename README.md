# ConText

## Table of Contents
1. Introduction
2. How to Use
    1. Preliminary Steps
    2. Usage and Descriptions
3. Other Functionality
    1. database_app.py
    2. userCreation.py

## Introduction
ConText allows you to simulate a messaging platform where users can send messages to other users on the platform in conversations.  The sending history of the users will determine what language they will receive messages in.  This is all done automatically with no user input, creating a seamless user experience.  

The language decision is based on three parameters
1. The receiver's sending history based on the language of all messages they have sent on the platform
2. The receiver's sending history based on the languages of messages they have sent in the conversation they are receiving a message in
3. The language of the last message the user sent in the conversation

These three parameters make agressive decisions about which language to translate to, and allow for users to easily be receiving messages in one language for a particular conversation, and another language in a separate conversation, based on the context of those particular conversations.

In the event of a tie (all parameters suggest a different language), currently the language used in all messages sent on the platform is used as a tiebreaker

## How to Use

### Preliminary Steps
There are a few preliminary steps in order to use ConText.  

You must have the context.db database created.  It is easiest to track how ConText is being used by starting with an empty database, so we recommend deleting context.db, and then creating the tables.  Creating the tables can be done by calling database_helper.create_tables(), which can easily be ran by launching database_app.py and following the instructions.

Once you have the database set up, you are ready to use ConText.

### Usage and Descriptions
We recommend running demo2.py, this will give you a straightforward interface for using ConText.  We will explain each command.

Creating a new user will create a row in user and sent_history to keep track of data for that user.  In sent_history, we keep track of all messages sent by the user in the row where the sent_it is equal to the negative of the user_id.

Creating a new conversation will allow two users to exchange messages with each other.  This will create two rows in sent_history, one for each user, which will keep track of the language of messages that user sends in this particular conversation.  By referencing the data in this row and for that user's row, we can make a decision on what language to translate to when that user receives a message.

Printing context parameters for a conversation will show what is determing the decision language when the user associated with this side of the conversation's sending history would receive a message in this conversation.

Finding users in a conversation will provide you with the user_ids of a users in that conversation.

Finding all conversations a user is in will allow you to provide a user_id and get all of the sent_ids associated with that user.

Sending a text in a conversation will allow one user to send a message to another user that they are in a conversation with.  You specify the sent_id that the message is being sent in, and then you are given the option to type in or generate a message.  You then are asked what language you would like to send the message in.  This allows you to manually generate interesting user data with a variety of languages with ease.  Then, the decision based on the user's parameters will be made, and the message will be printed in that decided language.  The sender's history will be automatically updated as well.

## Other functionality

database_app.py has a separate interface you can use to interact with the backend of the project.  There is nothing here that you can't do in demo2.py, so we recommend using demo2.py

userCreation.py can be run to create the tables and generate a bunch of conversations, with users that speak 1-5 languages.  This is what we used in order to generate training data.  If you would like to generate training data for your own purposes, we recommend running this, otherwise, if you just want to develop an understanding of the system, manually running demo2.py is the recommended way.