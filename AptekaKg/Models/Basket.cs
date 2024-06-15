namespace AptekaKg.Models
{
	public class Basket
	{
		public int Id { get; set; }
		public User User { get; set; }
		public string UserId { get; set; }
		public Medicine Medicine { get; set; }
		public int MedicineId { get; set; }
	}
}
