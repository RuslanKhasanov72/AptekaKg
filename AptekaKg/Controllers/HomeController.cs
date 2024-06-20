using AptekaKg.Models;
using AptekaKg.utils;
using AptekaKg.ViewModels;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Diagnostics;
using System.Linq;

namespace AptekaKg.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;
		private readonly ElasticSearchService _elasticsearchService;

		private UsersContext _db;

        public HomeController(UsersContext db, ILogger<HomeController> logger)
        {
            _db = db;
            _logger = logger;
			_elasticsearchService = new ElasticSearchService();
		}


        public async Task<IActionResult> Index(string query=null, int page = 1)
        {
            int pageSize = 12;
            var categorylist = _db.Categories.ToList();
            IQueryable<Medicine> medpages = _db.Medicines;
            var subcategorylist = _db.SubCategories.ToList();
            var count = await medpages.CountAsync();
            var items = await medpages.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
            PageViewModel pageViewModel = new PageViewModel(count, page, pageSize);
            if(query!=null)
            {
				var results = _elasticsearchService.SearchMedicines(query);
                items=results.ToList();
			}
			HomeConModel model = new HomeConModel
            {
                Categories = categorylist,
                SubCategories = subcategorylist,
                PageViewModel = pageViewModel,
                Medicines = items

            };
            return View(model);
        }
        [HttpPost]
		public JsonResult Search(string searchValue)
		{
			if(string.IsNullOrWhiteSpace(searchValue))
                return Json(1);
			var searchResults = _elasticsearchService.SearchMedicines(searchValue,8);
            return Json(searchResults);
		}

		public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
