using AptekaKg.Models;

namespace AptekaKg.ViewModels
{
	public class MainPageViewModel
	{
		public Medicine Medicine { get; set; }
		public IEnumerable<Category> Categories { get; set; }
		public IEnumerable<SubCategory> SubCategories { get; set; }
		public IEnumerable<Pharmacy> Pharmacies { get; set; }
	}
}
