using AptekaKg.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using OpenQA.Selenium.Chrome;
using OpenQA.Selenium;
using System.Security.Claims;
using AptekaKg.ViewModels;
using System.Collections.Generic;

namespace AptekaKg.Controllers
{
	public class AccountController : Controller
	{
		public UsersContext _db;
		private readonly UserManager<User> _userManager;
		private readonly SignInManager<User> _signInManager;

		public AccountController(UserManager<User> userManager, SignInManager<User> signInManager, UsersContext db)
		{
			_userManager = userManager;
			_signInManager = signInManager;
			_db = db;
		}
		[HttpGet]
		public IActionResult Register()
		{
			var subcategorylist = _db.SubCategories.ToList();
			var categorylist = _db.Categories.ToList();
			RegisterViewModel model = new RegisterViewModel
			{
				Categories = categorylist,
				SubCategories = subcategorylist
			};
			return View(model);
		}
		[HttpPost]
		public async Task<IActionResult> Register(RegisterViewModel model)
		{
			var subcategorylist = _db.SubCategories.ToList();
			var categorylist = _db.Categories.ToList();
			ModelState.Remove("Categories");
			ModelState.Remove("SubCategories");
			if (ModelState.IsValid)
			{
				User user = new User
				{
					Email = model.Email,
					UserName = model.Phone,
					Adress = model.Adress,
				};
				var result = await _userManager.CreateAsync(user, model.Password);
				//Создание пользователя средствами Identity на основе объекта пользователя и его пароля
				//Возвращает результат выполнения в случае успеха впускаем пользователя в систему
				if (result.Succeeded)
				{
					await _userManager.AddToRoleAsync(user, "user");
					await _signInManager.SignInAsync(user, false);
					return RedirectToAction("Index", "Home");
				}
				foreach (var error in result.Errors)
					ModelState.AddModelError(string.Empty, error.Description);
			}
			RegisterViewModel modell = new RegisterViewModel
			{
				Categories = categorylist,
				SubCategories = subcategorylist,
				Email = model.Email,
				Adress = model.Adress,
				Password = model.Password,
				PasswordConfirm = model.PasswordConfirm,
				Phone = model.Phone
			};
			return View(modell);
		}

		[HttpGet]
		public IActionResult Login()
		{
			var subcategorylist = _db.SubCategories.ToList();
			var categorylist = _db.Categories.ToList();
			LoginViewModel model = new LoginViewModel
			{
				Categories = categorylist,
				SubCategories = subcategorylist
			};
			return View(model);
		}
		[HttpPost]
		[ValidateAntiForgeryToken]
		public async Task<IActionResult> Login(LoginViewModel model)
		{
			var subcategorylist = _db.SubCategories.ToList();
			var categorylist = _db.Categories.ToList();
			ModelState.Remove("Categories");
			ModelState.Remove("SubCategories");
			if (ModelState.IsValid)
			{
				User user = await _userManager.FindByNameAsync(model.Login);
				if (user != null)
				{
					var result = await _signInManager.PasswordSignInAsync(
						user,
						model.Password,
						model.RememberMe,
						false
						);
					if (result.Succeeded)
					{
						return RedirectToAction("Index", "Home");
					}
				}
				ModelState.AddModelError("", "Неправильный логин и (или) пароль");
			}
			LoginViewModel modell = new LoginViewModel
			{ 
				Categories = categorylist,
				SubCategories = subcategorylist,
				Login = model.Login,
				Password = model.Password,
				RememberMe= model.RememberMe
			};
			return View(modell);
		}
		[HttpPost]
		[ValidateAntiForgeryToken]
		public async Task<IActionResult> LogOff()
		{
			await _signInManager.SignOutAsync();
			return RedirectToAction("Index", "Home");
		}
		[HttpPost]
		public async Task<IActionResult> Buy(double price)
		{
			var franchise =_db.Franchises.ToList();
			var Userreal = _db.Users.FirstOrDefault(x=>x.Id== User.FindFirst(ClaimTypes.NameIdentifier).Value);
			// Указываем путь к chromedriver.exe (предварительно скачанный и распакованный)
			// Это необходимо для запуска Chrome
			var driver = new ChromeDriver();

			// Открываем целевой сайт
			driver.Navigate().GoToUrl("https://zakaz.kg/");

			// Находим форму по её id (предположим, что id формы равен "form")
			var formElement = driver.FindElement(By.ClassName("Order-registration"));

			var phoneInput = formElement.FindElement(By.Name("phone"));
			phoneInput.SendKeys(Userreal.UserName);

			var toInput = formElement.FindElement(By.Name("delivery"));
			toInput.SendKeys(Userreal.Adress);


			var amountinput = formElement.FindElement(By.Name("amount"));
			amountinput.SendKeys(price.ToString());

			var bacsketlist = _db.Baskets.Where(x => x.UserId == Userreal.Id).ToList();
			List<int> medidss = new List<int>();
			foreach (var m in bacsketlist)
			{
				medidss.Add(m.MedicineId);
			}
			var medlist = _db.Medicines.Where(x => medidss.Contains(x.Id));
			string comment = "";
			List<string> pharmacys = new List<string>();
			foreach(var med in medlist)
			{
				string frann = ChangePharmName(med.Franchise.Name);
				if (!pharmacys.Contains(frann))
				{
					pharmacys.Add(frann);
				}
				comment += $"{med.Name} с аптеки {frann}, ";
			}
			var from = "";
			foreach (var fr in pharmacys)
			{
				from += $"Аптека {fr}";
			}
			var fromInput = formElement.FindElement(By.Name("pickup"));
			fromInput.SendKeys(from);
			var commentinput = formElement.FindElement(By.Name("comment"));
			commentinput.SendKeys(comment);

			

			return View();
		}
		public IActionResult Bascket()
		{
			var subcategorylist = _db.SubCategories.ToList();
			var categorylist = _db.Categories.ToList();
			var medicinesId = _db.Baskets.Where(x => x.UserId == User.FindFirst(ClaimTypes.NameIdentifier).Value);
			List<int> medidss=new List<int>();
			foreach(var m in medicinesId)
			{
				medidss.Add(m.MedicineId);
			}
			var medlist = _db.Medicines.Where(x => medidss.Contains(x.Id));
			double price = 0;
			foreach(var med in medlist)
			{
				price += med.Price;
			}
			ViewBag.Price = price;
			BacsketViewModel model = new BacsketViewModel
			{
				Categories = categorylist,
				SubCategories = subcategorylist,
				Medicines = medlist
				
			};
			return View(model);
		}

		public string ChangePharmName(string name)
		{
			switch (name)
			{
				case "ОсОО \"Неман\"":
					return "Неман";
				case "ОсОО \"Бимед Фарм\"":
					return "Бимед";
				case "ОсОО Лекарь":
					return "Лекарь";
			}

			return "";
		}
	}
}
