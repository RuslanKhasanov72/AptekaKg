using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace AptekaKg.Migrations
{
    /// <inheritdoc />
    public partial class AddNumberOrder : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<int>(
                name: "Count",
                table: "Orders",
                type: "integer",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<int>(
                name: "MedicineId",
                table: "Orders",
                type: "integer",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.AddColumn<int>(
                name: "NumberOfOrder",
                table: "Orders",
                type: "integer",
                nullable: false,
                defaultValue: 0);

            migrationBuilder.CreateIndex(
                name: "IX_Orders_MedicineId",
                table: "Orders",
                column: "MedicineId");

            migrationBuilder.AddForeignKey(
                name: "FK_Orders_Medicines_MedicineId",
                table: "Orders",
                column: "MedicineId",
                principalTable: "Medicines",
                principalColumn: "Id",
                onDelete: ReferentialAction.Cascade);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropForeignKey(
                name: "FK_Orders_Medicines_MedicineId",
                table: "Orders");

            migrationBuilder.DropIndex(
                name: "IX_Orders_MedicineId",
                table: "Orders");

            migrationBuilder.DropColumn(
                name: "Count",
                table: "Orders");

            migrationBuilder.DropColumn(
                name: "MedicineId",
                table: "Orders");

            migrationBuilder.DropColumn(
                name: "NumberOfOrder",
                table: "Orders");
        }
    }
}
