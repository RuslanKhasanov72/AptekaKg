using AptekaKg.Models;
namespace AptekaKg.utils
{
	public class DataMigrationService
	{
		private readonly UsersContext _db;
		private readonly ElasticSearchService _elasticsearchService;

		public DataMigrationService(UsersContext db)
		{
			_db = db;
			_elasticsearchService = new ElasticSearchService();
		}

		public void MigrateData()
		{
			var medicines = _db.Medicines.ToList();
			//_elasticsearchService.IndexMedicines(medicines);
		}
	}
}
