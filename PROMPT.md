# Web Appliation for data validation of data submitted by banks

## Application description
- There is a government entity called Banks Monitoring Office (BMO). BMO collects data from banks. This data is used to make economic policies and govern the banks. 


## User interface
- Analysts from the BMO will login to the app to do the work.
- When a user login, they will see a list of reports submitted by the banks. A report has information like: ABA code of the bank who submitted, report code, report submission date, a flag if the report data contains any errors, a flag if the report is accepted. 
- Users should be able to view report data validation errors for any report. 
- Users should be able to register comment on any errors. 
- Users should be able to accept or reject any report.

## Coding guidelines
- Keep code simple.
- Add enough console logs to help debugging the app.
- Keep all the frontend code contained in a single index.html file. 
- This is a demo application so do not worry about scalability, security and performance.

## Technology 
- Frontend is developed using a single HTML page using VueJS, Vuetify and VueRouter. 
- Backend is developed using Python using FastAPI
- Use sqlite file based database to store data. Since this is just a demo project, it is ok to put users and their passwords in the database as clear text.


## Seed data
- Create sevral users.
- Create 20 fake banks
- Create 30 fake reports submissions between date Jan 2025 till June 2025.
- Create some report data validation errors records. Some errors should have a comments, some are blank.


## Chatbot feaures
- User should be able to click on a floating chatbot icon (stored in client/images/chatbot.png) on bottom right, and open a chatbot user interface.
- When user type and send message, call an API to send it to the server main.py.
- For now, just echo as a reponse with "Echo: " prefix.

## MCP Agent
- mcp_agent.py is a agent that uses Model Context Protocol to use LLM.
- Convert it to use Bedrock model "anthropic.claude-3-5-sonnet-20240620-v1:0" instead of Ollama.

## MCP tools
- bmo_mcp_server.py file contains the MCP servers. 
- main.py is my API server.
- Create tools in my MCP server based on the api routes.


## SQL Runner MCP
- I want the user to ask questions that can be answered using SQL Queries. 
- For that, create MCP tool. 
- The MCP server should fetch complete db schema. 
- MCP server should expose a tool method that will return complete schema. 
- This schema will be used by LLM server so that it can generate proper SQL.
- MCP context should also tell what type of database system it is and what SQL dilect is expected. 
- Implement methods to fire any SQL statement and expose that as a tool.
- When you return answer that contains tabular data, ask LLM to format it using Markdown table specifications. 
- All the MCP tool methods should have detailed description so that LLM can understand.

## Sample MCP questions
- Add comment on the Bank of America report related to calculation error saying please double check the calculations.
- Do the latest report from sun trust contain errors?
- How many errors are in the report from Bank of America?
- Accept the latest report from Union Bnak.
- How many errors are in the report submitted by US Bank on March 14, 2025. 
- Get rejected reports
- The latest report from Capital One Bank contains a validation error for Regulatory Compliance on customer count. Add a comment: Customers count value can not be zero.
- List reports that do not have errors but are in pending state.
- List reports that do not have errors but are not still accepted.
    - Accept those 8 reports
- Delete citi bank
- Add bank 123123345, Sophia Bank
- Change the name of KeyBank to Key Bank
- Count the total reports that were submitted in the first week of March 2025
- Count the total reports that were submitted in the first 2 weeks of Jan 2025

