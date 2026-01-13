using Microsoft.AspNetCore.Mvc;
using RestAPI_CSharp.Models;
using System.Collections.Concurrent;

namespace RestAPI_CSharp.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class RowsController : ControllerBase
    {
        private static readonly ConcurrentDictionary<int, Row> rows = new();
        private static int nextId = 3;

        static RowsController()
        {
            rows[1] = new Row { Id = 1, Name = "Apples", Quantity = 10 };
            rows[2] = new Row { Id = 2, Name = "Oranges", Quantity = 5 };
        }

        [HttpGet]
        public ActionResult<IEnumerable<Row>> GetAll()
        {
            return Ok(rows.Values);
        }

        [HttpGet("{id}")]
        public ActionResult<Row> Get(int id)
        {
            if (!rows.TryGetValue(id, out var row))
                return NotFound(new { message = "Row not found" });
            return Ok(row);
        }

        [HttpPost]
        public ActionResult<Row> Create([FromBody] Row data)
        {
            if (string.IsNullOrWhiteSpace(data.Name))
                return BadRequest(new { message = "Missing 'name'" });
            var row = new Row { Id = nextId++, Name = data.Name, Quantity = data.Quantity };
            rows[row.Id] = row;
            return CreatedAtAction(nameof(Get), new { id = row.Id }, row);
        }

        [HttpPut("{id}")]
        public ActionResult<Row> Update(int id, [FromBody] Row data)
        {
            if (!rows.TryGetValue(id, out var row))
                return NotFound(new { message = "Row not found" });
            if (!string.IsNullOrWhiteSpace(data.Name))
                row.Name = data.Name;
            row.Quantity = data.Quantity;
            return Ok(row);
        }

        [HttpDelete("{id}")]
        public ActionResult<object> Delete(int id)
        {
            if (!rows.TryRemove(id, out var deleted))
                return NotFound(new { message = "Row not found" });
            return Ok(new { deleted });
        }
    }
}
