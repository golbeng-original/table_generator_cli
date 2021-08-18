using System;

namespace Generate
{
	public partial class GenerateTablesMeta
	{
		private static void InitalizeGenerateTableMeta()
		{
			TableMetaMapping.Add(typeof(TblPiadgoods), new TableMeta()
			{
				tableName = "TblPiadgoods",
				dbName = "Piadgoods.byte",
			});
			TableMetaMapping.Add(typeof(TblMoney), new TableMeta()
			{
				tableName = "TblMoney",
				dbName = "Money.byte",
			});
			TableMetaMapping.Add(typeof(TblTopping), new TableMeta()
			{
				tableName = "TblTopping",
				dbName = "Topping.byte",
			});
			TableMetaMapping.Add(typeof(TblFacility), new TableMeta()
			{
				tableName = "TblFacility",
				dbName = "Facility.byte",
			});
			TableMetaMapping.Add(typeof(TblExample_table), new TableMeta()
			{
				tableName = "TblExample_table",
				dbName = "Example_table.byte",
			});
			TableMetaMapping.Add(typeof(TblCustomer), new TableMeta()
			{
				tableName = "TblCustomer",
				dbName = "Customer.byte",
			});
		}
	}
}
