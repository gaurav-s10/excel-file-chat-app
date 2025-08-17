# Excel File Chat Application

- I have created 2 services (backend and frontend)
- Backend logic is in chatapp/consumer.py and endpoint for websocket interface is - ws/excel/
- Endpoint URL ```ws://localhost:8000/ws/excel/``` used in frontend for all the operations.

**Backend:** Django with Channels (for webscocket) and Redis, Pandas for excel file malipulations
**Frontend:** React 

---

## Workflow

- Upload Excel files via HTTP (`.xls`, `.xlsx`)
- Real-time operations (add/modify columns, get preview) via WebSocket chat interface
- Download processed Excel file

---

## Requirements

- [Docker](https://www.docker.com/) (with docker-compose) **OR**
  - Python 3.11+, pip, virtualenv
  - Node.js 18+
  - Redis server

---

## Getting Started (Docker Compose)

- Make sure Docker Desktop along with WSL is installed if in windows.  -- With Docker 
- Refer Dockerfile of both services to install dependencies and run services locally -- Without Docker

1. **Build and run all services:**
    ```
    docker-compose up --build
    ```

2. **Open your browser:**
    - Frontend: [http://localhost:3000](http://localhost:3000)
    - Backend API (if needed): [http://localhost:8000](http://localhost:8000)
    - Redis runs internally (no external access needed)



