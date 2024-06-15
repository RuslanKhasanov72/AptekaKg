using AptekaKg.Models;

namespace AptekaKg.ViewModels
{
	public class CategoryViewModel
	{
		public IEnumerable<Category> Categories { get; set; }
		public IEnumerable<SubCategory> SubCategories { get; set; }
		public IEnumerable<Medicine> Medicines { get; set; }
		public PageViewModel PageViewModel { get; set; }
	}
}
