using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AptekaKg.Migrations
{
    /// <inheritdoc />
    public partial class AddImageurlfranchise : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "ImageUrl",
                table: "Franchises",
                type: "text",
                nullable: true,
                defaultValue: "");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "ImageUrl",
                table: "Franchises");
        }
    }
}
