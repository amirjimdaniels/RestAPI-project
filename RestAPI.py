from flask import Flask, jsonify, request, render_template_string, abort

app = Flask(__name__)

# -----------------------------
# In-memory "database"
# -----------------------------
# Each row is: { "id": int, "name": str, "quantity": int }
rows = {}
next_id = 1


def get_next_id():
    global next_id
    nid = next_id
    next_id += 1
    return nid


# Seed with a couple of example rows
rows[1] = {"id": 1, "name": "Apples",  "quantity": 10}
rows[2] = {"id": 2, "name": "Oranges", "quantity": 5}
next_id = 3


# -----------------------------
# REST API (JSON)
# -----------------------------

@app.route("/api/rows", methods=["GET"])
def list_rows():
    """READ ALL: Return all rows as JSON."""
    return jsonify(list(rows.values()))


@app.route("/api/rows/<int:row_id>", methods=["GET"])
def get_row(row_id):
    """READ ONE: Return a single row by id."""
    row = rows.get(row_id)
    if row is None:
        abort(404, description="Row not found")
    return jsonify(row)


@app.route("/api/rows", methods=["POST"])
def create_row():
    """CREATE: Add a new row."""
    data = request.get_json()
    if not data or "name" not in data or "quantity" not in data:
        abort(400, description="Missing 'name' or 'quantity'")

    new_id = get_next_id()
    row = {
        "id": new_id,
        "name": data["name"],
        "quantity": int(data["quantity"])
    }
    rows[new_id] = row
    return jsonify(row), 201  # 201 Created


@app.route("/api/rows/<int:row_id>", methods=["PUT"])
def update_row(row_id):
    """UPDATE: Modify an existing row."""
    if row_id not in rows:
        abort(404, description="Row not found")

    data = request.get_json()
    if not data:
        abort(400, description="Missing JSON body")

    # Update only fields that are present
    if "name" in data:
        rows[row_id]["name"] = data["name"]
    if "quantity" in data:
        rows[row_id]["quantity"] = int(data["quantity"])

    return jsonify(rows[row_id])


@app.route("/api/rows/<int:row_id>", methods=["DELETE"])
def delete_row(row_id):
    """DELETE: Remove a row by id."""
    if row_id not in rows:
        abort(404, description="Row not found")

    deleted = rows.pop(row_id)
    return jsonify({"deleted": deleted})


# -----------------------------
# Simple HTML front-end
# -----------------------------

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>8-Puzzle REST Table Demo</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 2rem; }
    table { border-collapse: collapse; width: 400px; margin-bottom: 1rem; }
    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
    th { background: #f3f3f3; }
    input { margin: 0 4px 4px 0; }
    button { margin-right: 4px; }
  </style>
</head>
<body>
  <h1>CRUD on HTML Table (via Python REST API)</h1>

  <table id="rows-table">
    <thead>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Quantity</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <!-- rows inserted here -->
    </tbody>
  </table>

  <h2>Create / Update Row</h2>
  <form id="row-form">
    <input type="number" id="row-id" placeholder="ID (for update)" />
    <input type="text" id="row-name" placeholder="Name" required />
    <input type="number" id="row-quantity" placeholder="Quantity" required />
    <button type="submit">Save</button>
    <button type="button" id="clear-form">Clear</button>
  </form>

  <script>
    const tableBody = document.querySelector("#rows-table tbody");
    const form = document.getElementById("row-form");
    const idInput = document.getElementById("row-id");
    const nameInput = document.getElementById("row-name");
    const qtyInput = document.getElementById("row-quantity");
    const clearBtn = document.getElementById("clear-form");

    async function fetchRows() {
      const res = await fetch("/api/rows");
      const data = await res.json();
      renderTable(data);
    }

    function renderTable(rows) {
      tableBody.innerHTML = "";
      rows.forEach(row => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
          <td>${row.id}</td>
          <td>${row.name}</td>
          <td>${row.quantity}</td>
          <td>
            <button data-action="edit" data-id="${row.id}">Edit</button>
            <button data-action="delete" data-id="${row.id}">Delete</button>
          </td>
        `;

        tableBody.appendChild(tr);
      });
    }

    tableBody.addEventListener("click", async (e) => {
      const btn = e.target;
      const action = btn.getAttribute("data-action");
      const id = btn.getAttribute("data-id");

      if (!action || !id) return;

      if (action === "edit") {
        // Load row into form
        const res = await fetch(`/api/rows/${id}`);
        if (res.ok) {
          const row = await res.json();
          idInput.value = row.id;
          nameInput.value = row.name;
          qtyInput.value = row.quantity;
        }
      } else if (action === "delete") {
        if (!confirm("Delete this row?")) return;
        const res = await fetch(`/api/rows/${id}`, { method: "DELETE" });
        if (res.ok) {
          fetchRows();
        }
      }
    });

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      const name = nameInput.value.trim();
      const quantity = Number(qtyInput.value);
      const idVal = idInput.value.trim();

      if (!name || isNaN(quantity)) {
        alert("Name and Quantity are required.");
        return;
      }

      const body = JSON.stringify({ name, quantity });

      // If ID is provided, do PUT (update). Otherwise, POST (create).
      if (idVal) {
        const res = await fetch(`/api/rows/${idVal}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body
        });
        if (!res.ok) {
          alert("Error updating row");
        }
      } else {
        const res = await fetch("/api/rows", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body
        });
        if (!res.ok) {
          alert("Error creating row");
        }
      }

      // Refresh table and clear form
      await fetchRows();
      clearForm();
    });

    function clearForm() {
      idInput.value = "";
      nameInput.value = "";
      qtyInput.value = "";
    }

    clearBtn.addEventListener("click", clearForm);

    // Initial data load
    fetchRows();
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    """Serve the HTML page with the table that talks to our REST API."""
    return render_template_string(HTML_PAGE)


if __name__ == "__main__":
    # Install Flask with: pip install flask
    app.run(debug=True)
