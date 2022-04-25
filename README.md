
<!-- GETTING STARTED -->
## Getting Started

Instruction on setting up this project locally.

### Prerequisites

* npm
* anaconda
* git bash

### Installation

_Follow below steps to install backend. (Only Once)_

1. Clone the repo
   ```sh
   git clone https://github.com/thanujamaheepala/paradox-medvqa.git
   ```
2. Import conda environment using `environment.yml`
   ```sh
   conda env create --file environment.yml
   ```
3. Change Paths in `backend/pvqa_simulate.py`


_Follow below steps to install frontend. (Only Once)_

1. Open a terminal in `frontend` directory and Install react and other libraries
   ```sh
   npm i react
   npm install react-loader-spinner
   npm install d3-scale-chromatic
   ```
### Run

_Follow below steps to Run the backend._

1. Open a bash terminal in `backend` directory and activate the conda environment
   ```sh
   conda activate <envName>
   ```

2. Run the following commands
   ```sh
   export FLASK_APP=server
   export FLASK_ENV=development (If required)
   flask run
   ```

_Follow below steps to Run the frontend._

1. Open a terminal in `frontend` directory and run the following commands
   ```sh
   npm start
   ```
