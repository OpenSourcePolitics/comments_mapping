# Comments mapping
### Purpose
This repository aims to aggregate the Decidim separated exports: proposals and comments. 
It will map all the comments with their respective proposals. 
Two output formats are expected : .txt and .csv 
- txt : will display the data vertically and respect the structure of the participation with an indentation system
- csv : all the information relative to a proposal is stored in a row

Both of them will be stored in the directory ```/comments_mapping/dist```
## Getting started 
### Requirements 
- Docker
- Python >= 3.8
- Strongly recommended : a virtual environment manager

### Setup 
**One command execution** 
- clone the repository 
- if not already available : install Docker (see [here](https://docs.docker.com/get-docker/))
- to execute the container and retrieve the results of the mapping for the first configuration please use the command : ```make start```  
  at the root of the project.
- the results ```"mapping_proposals_comments.csv"``` and ```"mapping_proposals_comments.txt"``` will automatically be added to the directory 
 ```./comments_mapping/dist```  once you have executed the former instruction
  
Please note that if you want to see the results on the other configurations available in ```/test_data``` then you'll have to 
update the file called in main.py and replace the "1" in  ```df_proposals, df_comments = get_data(os.path.join(os.getcwd(),
                                                      "test_data/comments_config1.xls"),
                                         os.path.join(os.getcwd(),
                                                      "test_data/proposals_config1.xls"))``` with either 2 or 3. 


  
**Execution without Makefile**
  ```
    - docker build -t python-mapping .
    - docker run python-mapping
  ```
  **To run the tests on docker**
  ```
    - docker run -it python-mapping /bin/bash 
    - cd tests
    - pytest test_data_tree_structure.py
  ```
**Local execution**
- if you have python and pip already installed 
    - create an environment python
    - activate the env
    ```
    - pip install -r requirements.txt
    - python main.py
    - output files : mapping_proposals_comments.txt, mapping_proposals_comments.csv (./comments_mapping/dist)
    ```
    

    
### Next steps 
- [ ] CI
- [ ] Flask api 
- [ ] local tests with postman
- [ ] small interface


