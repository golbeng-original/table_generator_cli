enum TestEnum
{
	none,
	/// comment Value_1
	value_1,
	/// comment Value_2
	value_2,
}
enum TestEnum2
{
	/// None
	none,
	_1,
	_2,
	_3,
	/// XXX Comment
	xxx,
	yyy,
}
enum PaymentType
{
	/// None
	none,
	/// Cash
	cash,
	/// Gold
	gold,
	pay,
}
enum MoneyType
{
	none,
	moneytype_1,
	moneytype_2,
}

int getGenerateEnumIndex(dynamic value) {
	if (value is TestEnum) {
		return value.index;
	}
	if (value is TestEnum2) {
		return value.index;
	}
	if (value is PaymentType) {
		return value.index;
	}
	if (value is MoneyType) {
		return value.index;
	}
	return 0;
}
