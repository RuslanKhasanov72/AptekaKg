using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AptekaKg.Migrations
{
    /// <inheritdoc />
    public partial class AddImageUrlMedicine : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "ImageUrl",
                table: "Medicines",
                type: "text",
                nullable: false,
                defaultValue: "");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "ImageUrl",
                table: "Medicines");
        }
    }
}
