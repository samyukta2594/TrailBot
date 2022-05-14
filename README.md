# TrailBot
Rasa Project for recommending hiking trails. /n
Rasa version: 3.0.0
Get code from git in your folder
1. git clone https://github.com/samyukta2594/TrailBot.git

Anaconda
1. Install Anaconda
2. Create virtual environment:  conda create -n yourvirtualenv python=3.8 
3. Activate virtual enviroment: conda activate yourvirtualenv
4. Update pip:
   python -m pip uninstall pip
   python -m ensurepip
   python -m pip install -U pip
4. Navigate to the folder where git code is cloned (where requirements.text is there): Use cd folderpath
5. Install dependencies: pip install -r requirements.txt
6. Train : rasa train
7. Run rasa actions in another terminal: rasa run actions
8. Query the bot using conversation flows
