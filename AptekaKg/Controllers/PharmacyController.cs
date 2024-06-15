using Microsoft.AspNetCore.Mvc;

namespace AptekaKg.Controllers
{
    public class PharmacyController : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
