# Collect_data_web

Collect data from Brazilian courts' websites.

## Step with docker

    * Install docker: https://github.com/jobino/learning_docker

    * docker pull arjaraujo/collect-data-crawlers:data

    * Running docker: ./docker/access_docker.sh

    * Running shell file: ./settings.sh

    * Run: ./run.sh docker

    * If Error: Error: That port is already in use. Solution: kill -9 -1 in your terminal.

    * Otherwise access: localhost:8000.

## Step without docker

    * install pip with python3
    * curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    * python3 get-pip.py
    * pip install virtualenv
    * create a virtualenv. Suggestion name: "collect_env". Follow command -> (virtualenv collect_env -p python3)
    * source collect_env/bin/activate
    * pip install -r requirements.txt
    * Run: ./run.sh
