import './base_table_meta.dart';
import './table.g.dart';

void initializeTableMeta()
{
		GenerateTableMeta.addMeta<TblPiadgoods>(
		TableMeta()..dbName = 'Piadgoods.db'..tableName = 'TblPiadgoods');
		GenerateTableMeta.addMeta<TblMoney>(
		TableMeta()..dbName = 'Money.db'..tableName = 'TblMoney');
		GenerateTableMeta.addMeta<TblTopping>(
		TableMeta()..dbName = 'Topping.db'..tableName = 'TblTopping');
		GenerateTableMeta.addMeta<TblFacility>(
		TableMeta()..dbName = 'Facility.db'..tableName = 'TblFacility');
		GenerateTableMeta.addMeta<TblExample_table>(
		TableMeta()..dbName = 'Example_table.db'..tableName = 'TblExample_table');
		GenerateTableMeta.addMeta<TblCustomer>(
		TableMeta()..dbName = 'Customer.db'..tableName = 'TblCustomer');
}
