using System.ComponentModel.DataAnnotations;

namespace AptekaKg.Models
{
	public class LoginViewModel
	{
		[Required]
		[Display(Name = "Логин")]
		public string Login { get; set; }

		[Required]
		[Display(Name = "Пароль")]
		public string Password { get; set; }

		[Display(Name = "Запомнить?")]
		public bool RememberMe { get; set; }

		public IEnumerable<Category> Categories { get; set; }
		public IEnumerable<SubCategory> SubCategories { get; set; }
	}
}
