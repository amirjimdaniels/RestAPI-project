# REST API Project (Multi-Language)

A **REST API** project demonstrating full **CRUD** (Create, Read, Update, Delete) operations on an in-memory collection of rows, implemented in **three languages**:

- 🐍 **Python** (Flask)
- 🔷 **C#** (ASP.NET Core)
- ☕ **Java** (Spring Boot)

---

## Features

- **REST API** for managing rows (Create, Read, Update, Delete)
- **In-memory storage** (no database required)
- **Python version** includes a simple HTML + JavaScript frontend
- JSON-based communication

Each row has the structure:

```json
{
  "id": 1,
  "name": "Apples",
  "quantity": 10
}
```

---

## Project Structure

```
RestAPI-project/
├── RestAPI.py              # Python Flask implementation
├── RestAPI_CSharp/         # C# ASP.NET Core implementation
└── RestAPI_Java/           # Java Spring Boot implementation
```

---

## API Endpoints

| Method | Endpoint           | Description         |
|--------|--------------------|---------------------|
| GET    | `/api/rows`        | Get all rows        |
| GET    | `/api/rows/{id}`   | Get a row by ID     |
| POST   | `/api/rows`        | Create a new row    |
| PUT    | `/api/rows/{id}`   | Update a row by ID  |
| DELETE | `/api/rows/{id}`   | Delete a row by ID  |

---

## How to Run

### Python (Flask)

1. Install dependencies:
   ```bash
   pip install flask
   ```
2. Run the application:
   ```bash
   python RestAPI.py
   ```
3. Open `http://localhost:5000` in your browser

### C# (ASP.NET Core)

1. Install [.NET SDK](https://dotnet.microsoft.com/download)
2. Navigate to the C# project folder:
   ```bash
   cd RestAPI_CSharp
   ```
3. Run the application:
   ```bash
   dotnet run
   ```

### Java (Spring Boot)

1. Install Java 17+ and Maven
2. Navigate to the Java project folder:
   ```bash
   cd RestAPI_Java
   ```
3. Run the application:
   ```bash
   mvn spring-boot:run
   ```

---

## Requirements

| Language | Requirements                          |
|----------|---------------------------------------|
| Python   | Python 3.x, Flask                     |
| C#       | .NET 8.0 SDK                          |
| Java     | Java 17+, Maven                       |
