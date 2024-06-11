namespace AptekaKg.Models
{
    public class Medicine
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string URL { get; set; }
        public double Price { get; set; }
        public bool Available { get; set; }
        public string ImageUrl { get; set; }
        public string Description { get; set; }
        public Franchise Franchise { get; set; }
        public int FranchiseId { get; set; }
        public Category Category { get; set; }
        public int CategoryId { get; set; }
        public SubCategory SubCategory { get; set; }
        public int SubCategoryId { get; set;}

    }
}
