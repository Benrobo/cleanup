# CleanUp
A home made tools which enables me clean up a particular directory using just a command in python.

## From This

<img src="https://raw.githubusercontent.com/Benrobo/cleanup/master/screenshot/cleanup1.PNG">

## To This

<img src="https://raw.githubusercontent.com/Benrobo/cleanup/master/screenshot/clean2.PNG">


## Getting started

## Clone or download the repo

- [x] Clone the repo

    ```bash 
        git clone https://github.com/benrobo/cleanup
    ```
- [x] Install all packages found in `requirements.txt`

```py
    python -m pip install -U -r requirements.txt
```

- [x] Start the `main.py` file within the downloaded repo using some of the commands below

```py

    # list all usefull cleanup comands 

    py main.py -h | --help

    # clean up the file where this current directory is present.

    py main.py -rcd | --run-cd
    
    # cleanup this specified path (copy all files: default)

    py main.py -p | --path (/users/{username}/documents/test)

    # cleanup this specified path (move all files)

    py main.py -p | --path (/users/{username}/documents/test) --move
```