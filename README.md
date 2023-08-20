# Chess-Bot

---
## Description
Welcome to my project! This project is a Chess-Bot that plays using the Lichess API as a front-end. Currently, it uses an engine that uses a set of neural networks to determine the probabilities of available moves to walk the game tree. With this project, I aim to gain a better understanding of training Machine Learning Models and to produce a competent Chess Bot. 

---
## How to Run
1. Create a Lichess.com Bot Account. Instructions on how to do so can be found [here](https://lichess.org/api#tag/Bot/operation/botAccountUpgrade)
2. Create an API token for the Bot Account
3. Create a folder in the root directory called `secrets` and create a text file called `api_token.txt` and put your api token in the text file. 
4. Run the main.py file in `src/bot_main`

---
## Credits
* The data used to train the Neural Networks can be found in the [lichess.org open database](https://database.lichess.org/)
* The Neural Network architectures and training methods were inspired the approach described by Barak Oshri and Nishith Khandwala in their paper [Predicting Moves in Chess using Convolutional Neural Networks](http://cs231n.stanford.edu/reports/2015/pdfs/ConvChess.pdf).