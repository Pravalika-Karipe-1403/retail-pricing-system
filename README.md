# retail-pricing-system

Web application that would allow users to:  
Functional Requirements
•	Upload and persist pricing feeds from retail stores using CSV files which contain Store ID, SKU, Product Name, Price, Date
•	Search for pricing records using various criteria and be able to edit/save changes to any record
Non-Functional Requirements
•	Standard set of non-functional requirements you would expect a retail stores chain with 3000 stores across multiple countries

# Retail Pricing Management System

# Tech Stack:

Angular 17
FastAPI
MySQL

# Features:

CSV Upload
Search with filters
Pagination
Edit price/effective\_date
Audit history

# Setup Instructions:

# Frontend:

cd retail-pricing-system\\frontend\\retail-pricing-frontend
npm install
npm run start

# Backend:

cd retail-pricing-system\\frontend\\retail-pricing-api
pip install -r requirements.txt
uvicorn main:app --reload

Further detailed instructions are mentioned in 'retail-pricing-system\\backend\\retail-pricing-api\\app' Readme file

# Database:

Run retail-pricing-system\\database\\table\_creation\_scripts in SQL Workbench

# Author:

Pravalika Karipe

