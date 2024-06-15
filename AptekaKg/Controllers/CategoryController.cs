using AptekaKg.Models;
using AptekaKg.ViewModels;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace AptekaKg.Controllers
{
	public class CategoryController : Controller
	{
		private UsersContext _db;

		public CategoryController(UsersContext db)
		{
			_db = db;
		}
		public async Task<IActionResult> Index(int catid,int subcatid=0,int page=1)
		{
			int pageSize = 12;
			var categorylist = _db.Categories.ToList();
			IQueryable<Medicine> medpages;
			ViewBag.Categ = catid;
			ViewBag.Subcat = subcatid;
			if (subcatid == 0)
			{
				medpages = _db.Medicines.Where(x => x.CategoryId == catid);
				ViewBag.CategName = _db.Categories.FirstOrDefault(x => x.Id == catid).Name;
				ViewBag.SubcatName = " ";
			}
			else { 
				medpages= _db.Medicines.Where(x => x.SubCategoryId == subcatid);
				ViewBag.SubcatName = $"/{_db.SubCategories.FirstOrDefault(x => x.Id == subcatid).Name}";
				ViewBag.CategName = _db.SubCategories.FirstOrDefault(x => x.Id == subcatid).Category.Name;
			}
			var subcategorylist = _db.SubCategories.ToList();
			var count = await medpages.CountAsync();
			var items = await medpages.Skip((page - 1) * pageSize).Take(pageSize).ToListAsync();
			PageViewModel pageViewModel = new PageViewModel(count, page, pageSize);
			CategoryViewModel model = new CategoryViewModel
			{
				Categories = categorylist,
				SubCategories = subcategorylist,
				PageViewModel = pageViewModel,
				Medicines = items

			};
			return View(model);
		}
	}
}
