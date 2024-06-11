using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace AptekaKg.Models
{
    public class UsersContext : IdentityDbContext<User>
    {
        public DbSet<Category> Categories { get; set; }
        public DbSet<User> ContextUsers { get; set; }
        public DbSet<SubCategory> SubCategories { get; set; }
        public DbSet<Franchise> Franchises { get; set; }
        public DbSet<Pharmacy> Pharmacies { get; set; }
        public DbSet<Medicine> Medicines { get; set; }
        public DbSet<Order> Orders { get; set; }
        public DbSet<OrderMedicine> OrderMedicines {  get; set; } 
        public UsersContext(DbContextOptions<UsersContext> options)
             : base(options)
        {
        }
    }
}
