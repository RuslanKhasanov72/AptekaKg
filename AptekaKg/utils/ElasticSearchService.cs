using AptekaKg.Models;
using Elasticsearch.Net;
using Elasticsearch.Net.Specification.IndicesApi;
using Nest;
using Npgsql;

namespace AptekaKg.utils
{
	public class ElasticSearchService
	{
		private readonly ElasticClient _client;

		public ElasticSearchService()
		{
			var settings = new ConnectionSettings(new Uri("http://localhost:9200"))
				.DefaultIndex("medicines").RequestTimeout(TimeSpan.FromMinutes(5));
			_client = new ElasticClient(settings);
			if (_client == null)
			{
				throw new NullReferenceException("Failed to initialize ElasticClient.");
			}
		}

		//public async Task<BulkResponse> IndexMedicines(IEnumerable<Medicine> medicines)
		//{
			//var indexResponse =  _client.IndexMany(medicines);
			//if (!indexResponse.IsValid)
			//{
				// Обработка ошибок
				//throw new Exception("Failed to index documents: " + indexResponse.ServerError.Error.Reason);
			//}
			//return indexResponse;
		//}
		public IEnumerable<Medicine> SearchMedicines(string query,int value=0)
		{
			ISearchResponse<Medicine>searchResponse=new SearchResponse<Medicine>();
			if (value != 0)
			{
				 searchResponse = _client.Search<Medicine>(s => s
					.Query(q => q
						.MultiMatch(m => m
							.Query(query).Fuzziness(Fuzziness.Auto)
							.Fields(f => f
								.Field(p => p.Name)
								.Field(p => p.Description)
							)
						)
					).Size(value)
				);
			}
			else
			{
				 searchResponse = _client.Search<Medicine>(s => s
					.Query(q => q
						.MultiMatch(m => m
							.Query(query).Fuzziness(Fuzziness.Auto)
							.Fields(f => f
								.Field(p => p.Name)
								.Field(p => p.Description)
							)
						)
					)
				);
			}

			return searchResponse.Documents;
		}
	}
}
