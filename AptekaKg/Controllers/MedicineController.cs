using AptekaKg.Models;
using AptekaKg.ViewModels;
using Microsoft.AspNetCore.Mvc;
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
				MedicineId = medid
			};
			_db.Baskets.Add(basket);
			_db.SaveChanges();
			return Redirect("~/Medicine/MainPage/"+medid);
		}
	}
}
