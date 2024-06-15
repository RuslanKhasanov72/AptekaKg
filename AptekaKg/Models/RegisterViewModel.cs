using System.ComponentModel.DataAnnotations;

namespace AptekaKg.Models
{
	public class RegisterViewModel
	{
			[Required]
			[Display(Name = "Email")]
			public string Email { get; set; }
			[Required]
			[Display(Name = "Телефон")]
			public string Phone { get; set; }
			[Required]
			[Display(Name = "Телефон")]
			public string Adress { get; set; }
			[Required]
			[Display(Name = "Пароль")]
			public string Password { get; set; }
			[Required]
			[Compare("Password", ErrorMessage = "Пароли не совпадают")]
			[Display(Name = "Подтвердить пароль")]
			public string PasswordConfirm { get; set; }
		public IEnumerable<Category> Categories { get; set; }
		public IEnumerable<SubCategory> SubCategories { get; set; }
	}

}
