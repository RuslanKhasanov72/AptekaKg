using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AptekaKg.Migrations
{
    /// <inheritdoc />
    public partial class AddAvailableMedicine : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "Available",
                table: "Medicines",
                type: "boolean",
                nullable: false,
                defaultValue: false);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Available",
                table: "Medicines");
        }
    }
}
