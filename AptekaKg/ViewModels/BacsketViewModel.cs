using AptekaKg.Models;

namespace AptekaKg.ViewModels
{
	public class BacsketViewModel
	{
		public IEnumerable<Category> Categories { get; set; }
		public IEnumerable<SubCategory> SubCategories { get; set; }
		public IEnumerable<Medicine> Medicines { get; set; }
	}
}
