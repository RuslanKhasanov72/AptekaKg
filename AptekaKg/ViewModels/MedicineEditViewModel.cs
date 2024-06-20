using AptekaKg.Models;

namespace AptekaKg.ViewModels
{
    public class MedicineEditViewModel
    {
        public IEnumerable<Category> Categories { get; set; }
        public IEnumerable<SubCategory> SubCategories { get; set; }
        public Medicine Medicine { get; set; }
    }
}
