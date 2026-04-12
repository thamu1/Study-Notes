# 3-Tier Architecture Examples

Three-tier architecture separates an application into three logical tiers:
- **Presentation Tier** (Frontend) - User interface
- **Business Logic Tier** (Backend/API) - Application logic
- **Data Tier** (Database) - Data storage

This structure allows independent scaling and development of each tier.

---

## Example 1: Basic Python Flask + MySQL + Nginx

### Architecture Overview
```
Client → Nginx (Port 80) → Flask API (Port 5000) → MySQL Database (Port 3306)
```

### Project Structure
```
project/
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── docker-compose.yml
└── db/
    └── init.sql
```

### Step 1: Create Nginx Dockerfile
**nginx/Dockerfile**
```dockerfile
FROM nginx:latest
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
```

### Step 2: Create Nginx Configuration
**nginx/nginx.conf**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream backend {
        server backend:5000;
    }

    server {
        listen 80;
        server_name localhost;

        location / {
            proxy_pass http://backend;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }

        location /api/ {
            proxy_pass http://backend/api/;
        }
    }
}
```

### Step 3: Create Flask Application
**backend/app.py**
```python
from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host='mysql-db',
        user='root',
        password='password',
        database='appdb'
    )

@app.route('/')
def index():
    return jsonify({"message": "Welcome to Flask API"})

@app.route('/api/users')
def get_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({"users": users})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**backend/requirements.txt**
```
Flask==2.3.0
mysql-connector-python==8.0.33
```

**backend/Dockerfile**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

### Step 4: Create docker-compose.yml
**docker-compose.yml**
```yaml
version: '3.8'

services:
  # Database Tier
  mysql-db:
    image: mysql:8
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: appdb
    ports:
      - "3306:3306"
    volumes:
      - db_data:/var/lib/mysql
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Business Logic Tier
  backend:
    build: ./backend
    container_name: flask-api
    environment:
      DB_HOST: mysql-db
      DB_USER: root
      DB_PASSWORD: password
      DB_NAME: appdb
    depends_on:
      mysql-db:
        condition: service_healthy
    networks:
      - app-network
    restart: on-failure

  # Presentation Tier
  nginx:
    build: ./nginx
    container_name: nginx-proxy
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network
    restart: on-failure

volumes:
  db_data:

networks:
  app-network:
    driver: bridge
```

### Step 5: Database Initialization
**db/init.sql**
```sql
USE appdb;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
('John Doe', 'john@example.com'),
('Jane Smith', 'jane@example.com');
```

### Step 6: Run the Application
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
# Navigate to http://localhost in your browser
# API endpoint: http://localhost/api/users

# Stop services
docker-compose down
```

---

## Example 2: Node.js + PostgreSQL + Redis + Nginx

### Architecture Overview
```
Client → Nginx (Port 80) → Node.js Express (Port 3000) + Redis Cache (Port 6379) ← PostgreSQL (Port 5432)
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  # Database Tier
  postgres:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: secret123
      POSTGRES_DB: myapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U admin"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Cache Tier
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Business Logic Tier
  backend:
    build: ./backend
    container_name: nodejs-api
    environment:
      NODE_ENV: production
      DB_HOST: postgres
      DB_USER: admin
      DB_PASSWORD: secret123
      DB_NAME: myapp
      REDIS_URL: redis://redis:6379
    ports:
      - "3000:3000"
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - app-network
    restart: on-failure

  # Presentation Tier
  nginx:
    image: nginx:latest
    container_name: nginx-reverse-proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - backend
    networks:
      - app-network
    restart: on-failure

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

### Node.js Backend
**backend/Dockerfile**
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
EXPOSE 3000
CMD ["node", "server.js"]
```

**backend/server.js**
```javascript
const express = require('express');
const { Pool } = require('pg');
const redis = require('redis');

const app = express();
app.use(express.json());

// Configure PostgreSQL
const pool = new Pool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
});

// Configure Redis
const redisClient = redis.createClient({
  url: process.env.REDIS_URL
});

redisClient.connect();

// Routes
app.get('/api/products', async (req, res) => {
  try {
    // Check Redis cache first
    const cachedData = await redisClient.get('products');
    if (cachedData) {
      return res.json({ source: 'cache', data: JSON.parse(cachedData) });
    }

    // Query database if not in cache
    const result = await pool.query('SELECT * FROM products');
    
    // Store in cache for 1 hour
    await redisClient.setEx('products', 3600, JSON.stringify(result.rows));
    
    res.json({ source: 'database', data: result.rows });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

---

## Example 3: Java Spring Boot + MySQL + RabbitMQ + Nginx

### Architecture Overview
```
Client → Nginx (Port 80) → Spring Boot (Port 8080) → MySQL (Port 3306)
                                   ↓
                            RabbitMQ (Port 5672)
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  # Database Tier
  mysql:
    image: mysql:8
    container_name: mysql-db
    environment:
      MYSQL_ROOT_PASSWORD: root123
      MYSQL_DATABASE: springdb
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Message Queue Tier
  rabbitmq:
    image: rabbitmq:3-management-alpine
    container_name: rabbitmq-broker
    environment:
      RABBITMQ_DEFAULT_USER: guest
      RABBITMQ_DEFAULT_PASS: guest
    ports:
      - "5672:5672"          # AMQP
      - "15672:15672"        # Management UI
    volumes:
      - rabbitmq_data:/var/lib/rabbitmq
    networks:
      - app-network
    healthcheck:
      test: ["CMD", "rabbitmq-diagnostics", "-q", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  # Business Logic Tier
  spring-api:
    build: ./backend
    container_name: spring-boot-api
    environment:
      SPRING_DATASOURCE_URL: jdbc:mysql://mysql:3306/springdb
      SPRING_DATASOURCE_USERNAME: root
      SPRING_DATASOURCE_PASSWORD: root123
      SPRING_RABBITMQ_HOST: rabbitmq
      SPRING_RABBITMQ_PORT: 5672
    ports:
      - "8080:8080"
    depends_on:
      mysql:
        condition: service_healthy
      rabbitmq:
        condition: service_healthy
    networks:
      - app-network
    restart: on-failure

  # Presentation Tier
  nginx:
    image: nginx:latest
    container_name: nginx-gateway
    ports:
      - "80:80"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - spring-api
    networks:
      - app-network
    restart: on-failure

volumes:
  mysql_data:
  rabbitmq_data:

networks:
  app-network:
    driver: bridge
```

---

## Example 4: React Frontend + FastAPI Backend + MongoDB

### Architecture Overview
```
Client → React Frontend (Port 3000) → FastAPI Backend (Port 8000) → MongoDB (Port 27017)
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  # Database Tier
  mongodb:
    image: mongo:6
    container_name: mongodb-db
    environment:
      MONGO_INITDB_ROOT_USERNAME: admin
      MONGO_INITDB_ROOT_PASSWORD: password123
      MONGO_INITDB_DATABASE: myapp
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db
      - ./db/init-mongo.js:/docker-entrypoint-initdb.d/init-mongo.js
    networks:
      - app-network
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5

  # Business Logic Tier
  fastapi:
    build: ./backend
    container_name: fastapi-api
    environment:
      MONGODB_URL: mongodb://admin:password123@mongodb:27017/myapp?authSource=admin
    ports:
      - "8000:8000"
    depends_on:
      mongodb:
        condition: service_healthy
    networks:
      - app-network
    restart: on-failure

  # Presentation Tier
  frontend:
    build: ./frontend
    container_name: react-frontend
    environment:
      REACT_APP_API_URL: http://localhost:8000
    ports:
      - "3000:3000"
    depends_on:
      - fastapi
    networks:
      - app-network
    restart: on-failure

volumes:
  mongo_data:

networks:
  app-network:
    driver: bridge
```

### FastAPI Backend
**backend/Dockerfile**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**backend/main.py**
```python
from fastapi import FastAPI
from mongoengine import connect, Document, StringField, IntField
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Connect to MongoDB
@app.on_event("startup")
async def startup():
    app.mongodb_client = AsyncIOMotorClient("mongodb://admin:password123@mongodb:27017/myapp?authSource=admin")
    app.database = app.mongodb_client.myapp

@app.on_event("shutdown")
async def shutdown():
    app.mongodb_client.close()

@app.get("/")
async def root():
    return {"message": "FastAPI 3-Tier Application"}

@app.get("/api/items")
async def get_items():
    items_collection = app.database.items
    items = await items_collection.find().to_list(None)
    return {"items": items}

@app.post("/api/items")
async def create_item(name: str, description: str):
    items_collection = app.database.items
    item = {"name": name, "description": description}
    result = await items_collection.insert_one(item)
    return {"id": str(result.inserted_id), **item}
```

### React Frontend
**frontend/Dockerfile**
```dockerfile
FROM node:18-alpine as build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:latest
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 3000
```

---

## Key Takeaways for 3-Tier Architecture

### Advantages
✅ **Separation of Concerns** - Each tier has a specific responsibility  
✅ **Scalability** - Scale individual tiers independently  
✅ **Maintainability** - Easier to update and debug  
✅ **Security** - Database not directly exposed to clients  
✅ **Reusability** - Backend can serve multiple frontends  

### Common Patterns
- Use custom networks for container communication
- Implement health checks for dependencies
- Use `depends_on` with `condition` for proper startup order
- Separate concerns into different containers
- Use environment variables for configuration
- Implement proper logging and monitoring

### Communication Flow
```
Frontend (Port 3000/80) 
   ↓
Backend API (Port 5000/8000/8080) 
   ↓
Database (Port 3306/5432/27017)
```

### Best Practices
1. **Isolation**: Keep database container on private network
2. **Health Checks**: Ensure services are ready before dependent services start
3. **Environment Variables**: Configuration should not be hardcoded
4. **Volumes**: Persistent data should use named volumes
5. **Resource Limits**: Set memory and CPU limits for each service
6. **Logging**: Centralize logs for debugging
