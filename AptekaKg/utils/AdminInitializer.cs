using AptekaKg.Models;
using Microsoft.AspNetCore.Identity;

namespace AptekaKg.utils
{
    public class AdminInitializer
    {
        public static async System.Threading.Tasks.Task SeedAdminUser(
          RoleManager<IdentityRole> _roleManager,
          UserManager<User> _userManager)
        {
            string adminEmail = "admin@admin.com";
            string adminPassword = "123_Aa";

            var roles = new[] { "admin", "user" };
            foreach (var role in roles)
            {
                if (await _roleManager.FindByNameAsync(role) is null)
                    await _roleManager.CreateAsync(new IdentityRole(role));
            }
            if (await _userManager.FindByNameAsync(adminEmail) == null)
            {
                User admin = new User { Email = adminEmail, UserName = adminEmail,Adress="адрес" };
                IdentityResult result = await _userManager.CreateAsync(admin, adminPassword);
                if (result.Succeeded)
                    await _userManager.AddToRoleAsync(admin, "admin");
            }
        }
    }
}
