# Project Setup

Pre-Requisites
1)Install Folder retail-pricing-api inside backend folder

2)Create a virtual environment inside retail-pricing-api
    cmd: python -m venv .venv
  2.1)you will see .venv and app folder inside it.

3)Active the venv by running the below cmd.
    cmd: .venv\Scripts\Activate

4)Navigate to the app folder by using below cmd.
    cmd: cd app

    4.1)Run the below command to install the required packages
       cmd: pip install -r requirement.txt

       Note: If you install any new package, Generate the requirement file.
       cmd: pip freeze > requirement.txt

    # TO RUN THE PROJECT
    4.2)cmd: uvicorn main:app --reload or fastapi run dev
    4.3)Now in the terminal you can see "Uvicorn running on <URL>". click on the URL and add "/docs" at the end.
