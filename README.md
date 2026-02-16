# Azure DevOps Release Scripts Viewer



A Streamlit web application that lists and manages database migration scripts from Azure DevOps repositories. The app allows you to filter scripts by release version, view commit history, and export results to Excel.



## Features



- 🔍 \*\*Filter by Release\*\*: Select a release version and folder to view matching scripts

- 📊 \*\*Commit History\*\*: See who added each script and when

- 📥 \*\*Excel Export\*\*: Download filtered results as formatted Excel files

- 🔗 \*\*Direct Links\*\*: Click file names to open them directly in Azure DevOps

- 🎨 \*\*Modern UI\*\*: Clean, responsive interface with custom styling



## Project Structure



```

ado-db-files/

├── app.py                   # Entry point (thin orchestrator)

├── config.py                # Settings, constants, env loading

├── models.py                # Data classes (FileItem)

├── services/

│   ├── \_\_init\_\_.py

│   └── ado\_client.py        # Azure DevOps REST API client

├── ui/

│   ├── \_\_init\_\_.py

│   ├── styles.py            # All custom CSS

│   └── components.py        # Header, selectors, results

├── utils/

│   ├── \_\_init\_\_.py

│   └── excel\_export.py      # Excel generation utilities

├── .env.example             # Template for secrets

├── requirements.txt

└── README.md

```



## Setup



### 1. Clone the repository



```bash

git clone <your-repo-url>

cd ado-db-files

```



### 2. Install dependencies



```bash

pip install -r requirements.txt

```



### 3. Configure environment variables



Copy `.env.example` to `.env` and fill in your Azure DevOps details:



```bash

cp .env.example .env

```



Edit `.env` with your values:



```env

ADO\_ORG=https://dev.azure.com/YOUR\_ORG

ADO\_PROJECT=Your Project Name

ADO\_REPO=your-repository-name

ADO\_BRANCH=main

ADO\_PAT=your-personal-access-token

```



\*\*Note\*\*: Create a Personal Access Token (PAT) in Azure DevOps with \*\*Code → Read\*\* permissions.



### 4. Customize configuration



Edit `config.py` to match your repository structure:



- Update `RELEASES` list with your release versions

- Update `FOLDER\_MAP` with your folder paths



## Run



```bash

streamlit run app.py

```



The app will be available at `http://localhost:8501`



## How It Works



1\. \*\*Select Release \& Folder\*\*: Choose a release version and folder path from dropdowns

2\. \*\*Fetch Scripts\*\*: Click "Fetch Scripts" to query Azure DevOps API

3\. \*\*View Results\*\*: See filtered scripts in a formatted table with:

&nbsp;  - File name (clickable link to ADO)

&nbsp;  - Developer who added the file

&nbsp;  - Date added

4\. \*\*Export\*\*: Click "Download as Excel" to export results



## API Integration



The app uses Azure DevOps REST API:

- \*\*Git Items API\*\*: Lists files in repository folders

- \*\*Commits API\*\*: Retrieves commit history for each file



## Requirements



- Python 3.8+

- Azure DevOps account with repository access

- Personal Access Token (PAT) with Code → Read permissions



## Technologies Used



- \*\*Streamlit\*\*: Web framework

- \*\*Requests\*\*: HTTP client for Azure DevOps API

- \*\*Pandas\*\*: Data manipulation for Excel export

- \*\*OpenPyXL\*\*: Excel file generation



## License



This project is provided as-is for demonstration purposes.



## Contributing



Feel free to fork and customize for your own use case!



