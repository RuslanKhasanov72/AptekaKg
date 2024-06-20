using AptekaKg.Models;
using AptekaKg.ViewModels;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using System.Security.Claims;

namespace AptekaKg.Controllers
{
    public class MedicineController : Controller
    {
		private UsersContext _db;

		public MedicineController(UsersContext db)
		{
			_db = db;
		}
		public IActionResult Index()
        {
            return View();
        }
		public IActionResult MainPage(int id)
		{
			var pharmacy=_db.Pharmacies.ToList();
			var franchiseist=_db.Franchises.ToList();
			Medicine med = _db.Medicines.FirstOrDefault(u => u.Id == id);
			var categorylist = _db.Categories.ToList();
			var subcategory=_db.SubCategories.ToList();
			MainPageViewModel viewModel = new MainPageViewModel
			{
				Medicine = med,
				Categories = categorylist,
				SubCategories = subcategory,
				Pharmacies=pharmacy
			};
			return View(viewModel);
		}
		[HttpPost]
		public IActionResult Add(int medid)
		{
			var UserId = User.FindFirst(ClaimTypes.NameIdentifier).Value;
			Basket basket = new Basket()
			{
				UserId = UserId,
				MedicineId = medid,
				Count = 1
			};
			_db.Baskets.Add(basket);
			_db.SaveChanges();
			return Redirect("~/Medicine/MainPage/"+medid);
		}
		public IActionResult Edit(int id,int categoryid) { 
			Medicine medicine = _db.Medicines.FirstOrDefault(m => m.Id == id);
            var categorylist = _db.Categories.ToList();
            var subcategory = _db.SubCategories.ToList();
			ViewBag.Category= new SelectList(_db.Categories, "Id", "Name");
			ViewBag.Subcategory= new SelectList(_db.SubCategories.Where(s=>s.CategoryId==categoryid), "Id", "Name");
			ViewBag.Franchise= new SelectList(_db.Franchises, "Id", "Name");
			MedicineEditViewModel viewModel = new MedicineEditViewModel
            {
                Medicine = medicine,
                Categories = categorylist,
                SubCategories = subcategory
            };
            return View(viewModel);
		}
		[HttpGet]
		public JsonResult GetSubcategories(int categoryId)
		{
			var subcategories = _db.SubCategories.Where(s=>s.CategoryId==categoryId);
			return Json(subcategories);
		}
		[HttpPost]
		public async Task<JsonResult> EditMedicine(Medicine medicine)
		{
			var categorylist = _db.Categories.ToList();
			var subcategory = _db.SubCategories.ToList();
			var franchises = _db.Franchises.ToList();
			return Json("Success");
		}
	}
}
