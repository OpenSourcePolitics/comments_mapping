# Comments mapping
### Purpose
This repository aims to aggregate the Decidim separated exports: proposals and comments. 
It will map all the comments with their respective proposals. 
Two output formats are expected : .txt and .csv 
- txt : will display the data vertically and respect the structure of the participation with an indentation system
- csv : all the information relative to a proposal is stored in a row

Both of them will be stored in the directory ```/comments_mapping/dist```
## Getting started

### TLDR

```
make start
```

### Requirements 
- Docker
- Python >= 3.8
- Strongly recommended : a virtual environment manager
- **Tolerated file extensions** : .csv (separator is ;) / .xls

### Local and language management for proposals
In multilingual proposal export you'll have several columns constructed as such body/*local* where *local* is a language identifier (en/fr etc). 
If several columns are present the algorithm will only keep the French data by renaming the columns body/fr and title/fr 
as body and title respectively. 
If your file does not contain any french local please make sure that it has at least a column body, and a column title.
Otherwise, the script will not be able to run. 
### Setup 
**One command execution** 
- clone the repository 
- if not already available : install Docker (see [here](https://docs.docker.com/get-docker/))
- to execute the container and retrieve the results of the mapping for the first configuration please use the command : ```make start```  
  at the root of the project.
- the results ```"mapping_proposals_comments.csv"```, ```"mapping_proposals_comments.txt"``` and ```mapping_proposals_comments.docx``` will automatically be added to the directory 
 ```./comments_mapping/dist```  once you have executed the former instruction
  
  
**Check your result :**
  if you're under linux or Mac you can use the cd command to go into the dist directory and check for your files :
- ```cd dist``` -> go from comments_mapping to ./comments_mapping/dist
- ```cd ..``` -> come back to the upper directory for example from ./comments_mapping/dist to ./comments_mapping


You can also just investigate the directories and files with you usual file system.
  
**Run on your own files**
- add the files you want to map together in the directory : ```./comments_mapping/test_data ```
- update the file called in main.py here : ```df_proposals, df_comments = get_data(os.path.join(os.getcwd(),
                                                      "root_path/YOUR_COMMENTS_FILE.csv"),
                                         os.path.join(os.getcwd(),
                                                      "root_path/YOUR_PROPOSALS_FILE.csv"))```
  
Please note that if you do not have personal data to execute the script on you can use the three configurations available in 
```./test_data``` to see it in action. 
You'll just have to change the files called in the main as explained before.

**USE A SORTING ARGUMENT**

In order to ease your work on these files a sorting properties were also implemented. 
Thus, you'll be able to choose between to arguments to sort the order in which the proposals will be displayed. 
In the function ```init_csv()```, ```init_txt()``` and ```init_docx```, you can add an argument "sorting_attribute"
- write **commentaires** if you want to display the proposals which received the higher number of comments 
- write **supports** if you want to see first the proposals which received the higher number of endorsements

Additional Note : by default the proposals will be displayed as if the argument "commentaires" was passed to the function.
It means that you'll see the most commented proposals first. Use the instructions above to change this behaviour. 
  
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
- [ ] multilingual exports  
- [x] CI


