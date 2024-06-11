namespace AptekaKg.Models
{
    public class OrderMedicine
    {
        public int Id { get; set; }
        public Order Order { get; set; }
        public int OrderId { get; set; }
        public Medicine Medicine { get; set; }
        public int MedicineId { get; set; }
    }
}
