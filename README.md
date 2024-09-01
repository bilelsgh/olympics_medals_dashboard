## Paris olympics dashboard

This project aims to visualize relevant information about the Paris 2024 Olympics thanks to an interactive and intuitive dashboard.
It covers the whole process from the data fetching, the dataset construction and the visualization.

### Main workflow
![alt text](https://github.com/bilelsgh/olympics_medals_dashboard)

### Run

1. Set the global variables in ``config/conf.yaml``
2. ```bash
    streamlit run dashboard.pu 
    ```

### Architecture
- ``config/``
  - ``conf.yaml``: Contains the modifiable parameters 
  - ``config.py``: Set the global variables
  

- ``datasets/``: Olympics medals datasets built 

- ``dashboard.py``: Streamlit dashboard to visualize data

- ``extract.py``: Functions to get the data and build the dataset

- ``process.py``: Functions to clean and process the data