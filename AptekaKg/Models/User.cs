using Microsoft.AspNetCore.Identity;

namespace AptekaKg.Models
{
    public class User: IdentityUser
    {
        public string Adress { get;set; }
        public string Name { get; set; }
        public string Surname { get; set; }
    }
}
