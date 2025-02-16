# Human Detection Project

## Overview

This project consists of a **FastAPI** backend, a **Next.js** frontend, and a **PostgreSQL** database, designed for human detection in images.

## Features

- Upload an image via the frontend
- Process the image using a lightweight object detection model
- Return the processed image with bounding boxes and the number of detected humans
- Store the results in a PostgreSQL database
- Logs system for tracking API activity
- Deployment using Docker

---

## Docker Deployment

### **Build & Run Docker Containers**

1. Navigate to the project root directory:
   ```sh
   cd human-detection
   ```
2. Build and start the services:
   ```sh
   docker-compose up --build
   ```
3. The application will be accessible at:
   - Backend: `http://localhost:8000/docs`
   - Frontend: `http://localhost:3000`
   - Database: PostgreSQL running in the container

### **Stopping Containers**

```sh
docker-compose down
```

---

## 5️⃣ Logging System

Logs are stored in `backend/logs/app.log`. You can check logs by running:

```sh
tail -f backend/logs/app.log
```

---

## Troubleshooting

- **CORS issues?** Ensure your backend allows requests from the frontend domain.
- **Database connection errors?** Verify PostgreSQL is running and credentials are correct.
- **Frontend not loading?** Check `FRONTEND_URL` in `.env`.

---

## Author

Developed by Le Nguyen Gia Bao.
