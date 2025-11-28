# Python REST API with HTML Table (Flask)

A simple **Python REST API** built with **Flask** that performs full **CRUD** (Create, Read, Update, Delete) operations on an in-memory collection of rows, and displays them in an **HTML table**.

The frontend is a minimal HTML page that uses JavaScript `fetch()` calls to talk to the API and updates the table without reloading the page.

---

## Features

- **REST API** for managing rows:
  - Create, read, update, delete
- **In-memory storage** (no database required)
- Simple **HTML + JavaScript** frontend:
  - Displays rows in a table
  - Form to create/update rows
  - Buttons to edit/delete each row
- JSON-based communication between frontend and backend

Each row has the structure:

```json
{
  "id": 1,
  "name": "Apples",
  "quantity": 10
}
