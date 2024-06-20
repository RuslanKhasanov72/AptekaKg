namespace AptekaKg.Models
{
    public class Order
    {
        public int Id { get; set; }
        public User User { get; set; }
        public string UserId { get; set; }
        public int Price { get; set; }
        public Medicine Medicine { get; set; }
        public int MedicineId { get; set; }
        public int NumberOfOrder { get; set; }
        public int Count { get; set; }
        public DateTime Created { get; set; }

    }
}
