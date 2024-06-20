using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AptekaKg.Migrations
{
    /// <inheritdoc />
    public partial class AddCountBascket : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "Count",
                table: "Baskets",
                type: "integer",
                nullable: false,
                defaultValue: 0);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Count",
                table: "Baskets");
        }
    }
}
