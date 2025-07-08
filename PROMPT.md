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