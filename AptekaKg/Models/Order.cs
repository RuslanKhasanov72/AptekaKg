namespace AptekaKg.Models
{
    public class Order
    {
        public int Id { get; set; }
        public User User { get; set; }
        public string UserId { get; set; }
        public int Price { get; set; }
    }
}
