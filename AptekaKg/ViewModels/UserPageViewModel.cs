using AptekaKg.Models;

namespace AptekaKg.ViewModels
{
	public class UserPageViewModel
	{

		public IEnumerable<Category> Categories { get; set; }
		public IEnumerable<SubCategory> SubCategories { get; set; }
		public User User { get; set; }
		public IEnumerable<List<Order>> OrderList { get; set; }
	}
}
