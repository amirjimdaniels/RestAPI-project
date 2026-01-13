using Microsoft.AspNetCore.Mvc;

namespace RestAPI_CSharp.Controllers
{
    [Route("")]
    public class HomeController : Controller
    {
        [HttpGet]
        public ContentResult Index()
        {
            // Serve the same HTML as the Python app
            var html = System.IO.File.ReadAllText("../RestAPI.py"); // Placeholder: Replace with actual HTML
            return Content(html, "text/html");
        }
    }
}
