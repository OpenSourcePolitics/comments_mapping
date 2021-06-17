# Comments mapping
###Purpose
This repository aims to aggregate the Decidim separated exports: proposals and comments. 
It will map all the comments with their respective proposals. 
Two output formats are expected : .txt and .csv 
- txt : will display the data vertically and respect the structure of the participation with an indentation system
- csv : all the information relative to a proposal is stored in a row

## Getting started 
###Requirements 
- Python >= 3.8
- Strongly recommended : a virtual environment manager

###Setup 
- clone the repository 
- if you have python and pip already installed 
    - create an environment python
    - activate the env
    ```
    - pip install -r requirements.txt
    - python main.py
    - output files : mapping_proposals_comments.txt, mapping_proposals_comments.csv (they will be stored in the folder test_data)
    ```
    
- run on docker:
  ```
    - docker build -t python-mapping .
    - docker run python-mapping
  or if you want to inspect the results
    - docker run -it python-mapping /bin/bash 
  ```
    
###Next steps 
- [ ] Flask api 
- [ ] local tests with postman
- [ ] small interface


