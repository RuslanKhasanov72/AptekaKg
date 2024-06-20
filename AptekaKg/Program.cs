using AptekaKg.Models;
using AptekaKg;
using Microsoft.AspNetCore.Identity;
using AptekaKg.utils;

public class Program
{
    public static async System.Threading.Tasks.Task Main(string[] args)
    {
		AppContext.SetSwitch("Npgsql.EnableLegacyTimestampBehavior", true);
		var host = CreateHostBuilder(args).Build();
        using var scope = host.Services.CreateScope();
        var services = scope.ServiceProvider;
        try
        {
            var userManager = services.GetRequiredService<UserManager<User>>();
            var rolesManager = services.GetRequiredService<RoleManager<IdentityRole>>();
            await AdminInitializer.SeedAdminUser(rolesManager, userManager);
		}
        catch (Exception ex)
        {
            var logger = services.GetRequiredService<ILogger<Program>>();
            logger.LogError(ex, "An error occurred while seeding the database.");
        }
        host.Run();
    }

    public static IHostBuilder CreateHostBuilder(string[] args) =>
        Host.CreateDefaultBuilder(args)
            .ConfigureWebHostDefaults(webBuilder =>
            {
                webBuilder.UseStartup<Startup>();
            });
}