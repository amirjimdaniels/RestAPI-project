# RestAPI_Java

This is a Java Spring Boot REST API implementation matching the structure of the C# RestAPI_CSharp project.

## How to Run

1. Make sure you have Java 17+ and Maven installed.
2. In this directory, run:
   
   mvn spring-boot:run

## Endpoints

- `GET /rows` - Get all rows
- `GET /rows/{id}` - Get a row by ID
- `POST /rows` - Add a new row (JSON body: {"id": int, "data": string})
- `DELETE /rows/{id}` - Delete a row by ID
