namespace AptekaKg.Models
{
    public class Pharmacy
    {
        public int Id { get; set; }
        public string Address { get; set; }
        public string Number { get; set; }
        public Franchise Franchise { get; set; }
        public int FranchiseId { get; set; }

    }
}
