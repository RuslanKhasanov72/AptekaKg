using Microsoft.EntityFrameworkCore;

namespace AptekaKg.Models
{
    public class UsersContext : IdentityDbContext<User>
    {
        public DbSet<FastFood> FastFoods { get; set; }
        public DbSet<User> ContextUsers { get; set; }
        public DbSet<Photo> Photos { get; set; }
        public DbSet<Review> Reviews { get; set; }
        public UsersContext(DbContextOptions<UsersContext> options)
             : base(options)
        {
        }
    }
}
