# User Study Server

The user study is implemented as a Flask web application. 

If you are just interested in the specific instructions given to the participant, you can find them in the html files in the templates/study/ directory. The order is start.html, instruction0.html, instruction1.html, submission_step.html, demographics.html, end.html.


# Running it locally

If you want to run the user study yourself, you can run it locally by installing Python 3.12, installing the required dependencies (see requirements.txt) and start it via

flask --app userstudy init-db
flask --app userstudy run --debug


# Running it remotely

If you want to run the user study on a remote server (like an AWS instance), the following steps are additionally needed:

Build it locally:
python -m build --wheel

Copy resulting file from the dist directory to your AWS node. Then run the following commands:

sudo dnf install tmux

mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm ~/miniconda3/miniconda.sh

source ~/miniconda3/bin/activate
conda init --all

conda create -n userstudy python=3.12
conda activate userstudy

pip install userstudy-1.0.2-py2.py3-none-any.whl
flask --app userstudy init-db

pip install waitress
waitress-serve --call 'userstudy:create_app'