import 'package:tuple/tuple.dart';
import './base_table.dart';
import '../enum/generate_enum.dart';

class TblPiadgoods extends TblBase
{
	int _primarykey= 0;
	int get primarykey => _primarykey;
	set primarykey(int value) {
		_primarykey = value;
		convertKey(_primarykey, true);
	}
	PaymentType paymentType = PaymentType.none;
	int quantity = 0;
	String productID = '';
	MoneyType goodtype1 = MoneyType.none;
	int goodquantity1 = 0;
	int goodbonusquantity1 = 0;
	MoneyType goodtype2 = MoneyType.none;
	int goodquantity2 = 0;
	int goodbonusquantity2 = 0;
	String paidgood_icon = '';

	@override
	int get propertiesCount => 11;
	@override
	Tuple2<String, Type> getPropertyInfo(int index) {
		switch (index) {
			case 0: return Tuple2('primarykey', primarykey.runtimeType);
			case 1: return Tuple2('paymentType', paymentType.runtimeType);
			case 2: return Tuple2('quantity', quantity.runtimeType);
			case 3: return Tuple2('productID', productID.runtimeType);
			case 4: return Tuple2('goodtype1', goodtype1.runtimeType);
			case 5: return Tuple2('goodquantity1', goodquantity1.runtimeType);
			case 6: return Tuple2('goodbonusquantity1', goodbonusquantity1.runtimeType);
			case 7: return Tuple2('goodtype2', goodtype2.runtimeType);
			case 8: return Tuple2('goodquantity2', goodquantity2.runtimeType);
			case 9: return Tuple2('goodbonusquantity2', goodbonusquantity2.runtimeType);
			case 10: return Tuple2('paidgood_icon', paidgood_icon.runtimeType);
		}
		return null;
	}

	@override
	bool setPropertyValueFromName<T>(String propertyName, T value) {
		if (propertyName.toLowerCase() == 'primarykey') {
			if (checkPropertyType(primarykey, value) == false) {
				 return false;
			}
		
			primarykey = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'paymenttype') {
			if (checkPropertyType(paymentType, value) == false) {
				 return false;
			}
		
			paymentType = value as PaymentType;
			return true;
		}
		if (propertyName.toLowerCase() == 'quantity') {
			if (checkPropertyType(quantity, value) == false) {
				 return false;
			}
		
			quantity = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'productid') {
			if (checkPropertyType(productID, value) == false) {
				 return false;
			}
		
			productID = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'goodtype1') {
			if (checkPropertyType(goodtype1, value) == false) {
				 return false;
			}
		
			goodtype1 = value as MoneyType;
			return true;
		}
		if (propertyName.toLowerCase() == 'goodquantity1') {
			if (checkPropertyType(goodquantity1, value) == false) {
				 return false;
			}
		
			goodquantity1 = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'goodbonusquantity1') {
			if (checkPropertyType(goodbonusquantity1, value) == false) {
				 return false;
			}
		
			goodbonusquantity1 = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'goodtype2') {
			if (checkPropertyType(goodtype2, value) == false) {
				 return false;
			}
		
			goodtype2 = value as MoneyType;
			return true;
		}
		if (propertyName.toLowerCase() == 'goodquantity2') {
			if (checkPropertyType(goodquantity2, value) == false) {
				 return false;
			}
		
			goodquantity2 = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'goodbonusquantity2') {
			if (checkPropertyType(goodbonusquantity2, value) == false) {
				 return false;
			}
		
			goodbonusquantity2 = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'paidgood_icon') {
			if (checkPropertyType(paidgood_icon, value) == false) {
				 return false;
			}
		
			paidgood_icon = value as String;
			return true;
		}
		return false;
	}
}
class TblMoney extends TblBase
{
	MoneyType _primarykey= MoneyType.none;
	MoneyType get primarykey => _primarykey;
	set primarykey(MoneyType value) {
		_primarykey = value;
		convertKey(_primarykey, true);
	}
	String name = '';
	int maxvalue = 0;
	String money_icon = '';

	@override
	int get propertiesCount => 4;
	@override
	Tuple2<String, Type> getPropertyInfo(int index) {
		switch (index) {
			case 0: return Tuple2('primarykey', primarykey.runtimeType);
			case 1: return Tuple2('name', name.runtimeType);
			case 2: return Tuple2('maxvalue', maxvalue.runtimeType);
			case 3: return Tuple2('money_icon', money_icon.runtimeType);
		}
		return null;
	}

	@override
	bool setPropertyValueFromName<T>(String propertyName, T value) {
		if (propertyName.toLowerCase() == 'primarykey') {
			if (checkPropertyType(primarykey, value) == false) {
				 return false;
			}
		
			primarykey = value as MoneyType;
			return true;
		}
		if (propertyName.toLowerCase() == 'name') {
			if (checkPropertyType(name, value) == false) {
				 return false;
			}
		
			name = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'maxvalue') {
			if (checkPropertyType(maxvalue, value) == false) {
				 return false;
			}
		
			maxvalue = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'money_icon') {
			if (checkPropertyType(money_icon, value) == false) {
				 return false;
			}
		
			money_icon = value as String;
			return true;
		}
		return false;
	}
}
class TblTopping extends TblBase
{
	int _primarykey= 0;
	int get primarykey => _primarykey;
	set primarykey(int value) {
		_primarykey = value;
		convertKey(_primarykey, true);
	}
	int _secondarykey= 0;
	int get secondarykey => _secondarykey;
	set secondarykey(int value) {
		_secondarykey = value;
		convertKey(_secondarykey, false);
	}
	String name = '';
	String description = '';
	String resource = '';
	ToppingType type = ToppingType.none;
	int open_rate_grade = 0;
	int open_Price_grade = 0;
	int get_rate_grade = 0;
	int get_price_grade = 0;

	@override
	int get propertiesCount => 10;
	@override
	Tuple2<String, Type> getPropertyInfo(int index) {
		switch (index) {
			case 0: return Tuple2('primarykey', primarykey.runtimeType);
			case 1: return Tuple2('secondarykey', secondarykey.runtimeType);
			case 2: return Tuple2('name', name.runtimeType);
			case 3: return Tuple2('description', description.runtimeType);
			case 4: return Tuple2('resource', resource.runtimeType);
			case 5: return Tuple2('type', type.runtimeType);
			case 6: return Tuple2('open_rate_grade', open_rate_grade.runtimeType);
			case 7: return Tuple2('open_Price_grade', open_Price_grade.runtimeType);
			case 8: return Tuple2('get_rate_grade', get_rate_grade.runtimeType);
			case 9: return Tuple2('get_price_grade', get_price_grade.runtimeType);
		}
		return null;
	}

	@override
	bool setPropertyValueFromName<T>(String propertyName, T value) {
		if (propertyName.toLowerCase() == 'primarykey') {
			if (checkPropertyType(primarykey, value) == false) {
				 return false;
			}
		
			primarykey = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'secondarykey') {
			if (checkPropertyType(secondarykey, value) == false) {
				 return false;
			}
		
			secondarykey = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'name') {
			if (checkPropertyType(name, value) == false) {
				 return false;
			}
		
			name = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'description') {
			if (checkPropertyType(description, value) == false) {
				 return false;
			}
		
			description = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'resource') {
			if (checkPropertyType(resource, value) == false) {
				 return false;
			}
		
			resource = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'type') {
			if (checkPropertyType(type, value) == false) {
				 return false;
			}
		
			type = value as ToppingType;
			return true;
		}
		if (propertyName.toLowerCase() == 'open_rate_grade') {
			if (checkPropertyType(open_rate_grade, value) == false) {
				 return false;
			}
		
			open_rate_grade = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'open_price_grade') {
			if (checkPropertyType(open_Price_grade, value) == false) {
				 return false;
			}
		
			open_Price_grade = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'get_rate_grade') {
			if (checkPropertyType(get_rate_grade, value) == false) {
				 return false;
			}
		
			get_rate_grade = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'get_price_grade') {
			if (checkPropertyType(get_price_grade, value) == false) {
				 return false;
			}
		
			get_price_grade = value as int;
			return true;
		}
		return false;
	}
}
class TblFacility extends TblBase
{
	int _primarykey= 0;
	int get primarykey => _primarykey;
	set primarykey(int value) {
		_primarykey = value;
		convertKey(_primarykey, true);
	}
	int _secondarykey= 0;
	int get secondarykey => _secondarykey;
	set secondarykey(int value) {
		_secondarykey = value;
		convertKey(_secondarykey, false);
	}
	String name = '';
	String description = '';
	String resource = '';
	FacilityType facilitytype = FacilityType.none;
	int get_rate = 0;
	InstallEffectType get_type = InstallEffectType.none;
	int get_value = 0;
	NeedType need_type = NeedType.none;
	int need_value = 0;
	int need_money = 0;
	int get_money = 0;
	bool enable_insert = true;

	@override
	int get propertiesCount => 14;
	@override
	Tuple2<String, Type> getPropertyInfo(int index) {
		switch (index) {
			case 0: return Tuple2('primarykey', primarykey.runtimeType);
			case 1: return Tuple2('secondarykey', secondarykey.runtimeType);
			case 2: return Tuple2('name', name.runtimeType);
			case 3: return Tuple2('description', description.runtimeType);
			case 4: return Tuple2('resource', resource.runtimeType);
			case 5: return Tuple2('facilitytype', facilitytype.runtimeType);
			case 6: return Tuple2('get_rate', get_rate.runtimeType);
			case 7: return Tuple2('get_type', get_type.runtimeType);
			case 8: return Tuple2('get_value', get_value.runtimeType);
			case 9: return Tuple2('need_type', need_type.runtimeType);
			case 10: return Tuple2('need_value', need_value.runtimeType);
			case 11: return Tuple2('need_money', need_money.runtimeType);
			case 12: return Tuple2('get_money', get_money.runtimeType);
			case 13: return Tuple2('enable_insert', enable_insert.runtimeType);
		}
		return null;
	}

	@override
	bool setPropertyValueFromName<T>(String propertyName, T value) {
		if (propertyName.toLowerCase() == 'primarykey') {
			if (checkPropertyType(primarykey, value) == false) {
				 return false;
			}
		
			primarykey = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'secondarykey') {
			if (checkPropertyType(secondarykey, value) == false) {
				 return false;
			}
		
			secondarykey = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'name') {
			if (checkPropertyType(name, value) == false) {
				 return false;
			}
		
			name = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'description') {
			if (checkPropertyType(description, value) == false) {
				 return false;
			}
		
			description = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'resource') {
			if (checkPropertyType(resource, value) == false) {
				 return false;
			}
		
			resource = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'facilitytype') {
			if (checkPropertyType(facilitytype, value) == false) {
				 return false;
			}
		
			facilitytype = value as FacilityType;
			return true;
		}
		if (propertyName.toLowerCase() == 'get_rate') {
			if (checkPropertyType(get_rate, value) == false) {
				 return false;
			}
		
			get_rate = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'get_type') {
			if (checkPropertyType(get_type, value) == false) {
				 return false;
			}
		
			get_type = value as InstallEffectType;
			return true;
		}
		if (propertyName.toLowerCase() == 'get_value') {
			if (checkPropertyType(get_value, value) == false) {
				 return false;
			}
		
			get_value = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'need_type') {
			if (checkPropertyType(need_type, value) == false) {
				 return false;
			}
		
			need_type = value as NeedType;
			return true;
		}
		if (propertyName.toLowerCase() == 'need_value') {
			if (checkPropertyType(need_value, value) == false) {
				 return false;
			}
		
			need_value = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'need_money') {
			if (checkPropertyType(need_money, value) == false) {
				 return false;
			}
		
			need_money = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'get_money') {
			if (checkPropertyType(get_money, value) == false) {
				 return false;
			}
		
			get_money = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'enable_insert') {
			if (checkPropertyType(enable_insert, value) == false) {
				 return false;
			}
		
			enable_insert = value as bool;
			return true;
		}
		return false;
	}
}
class TblExample_table extends TblBase
{
	TestEnum _primarykey= TestEnum.none;
	TestEnum get primarykey => _primarykey;
	set primarykey(TestEnum value) {
		_primarykey = value;
		convertKey(_primarykey, true);
	}
	String _secondarykey= '';
	String get secondarykey => _secondarykey;
	set secondarykey(String value) {
		_secondarykey = value;
		convertKey(_secondarykey, false);
	}
	int IntField1 = 0;
	String StringField2 = '';
	double FloatField3 = 0;
	TestEnum EnumField4 = TestEnum.none;

	@override
	int get propertiesCount => 6;
	@override
	Tuple2<String, Type> getPropertyInfo(int index) {
		switch (index) {
			case 0: return Tuple2('primarykey', primarykey.runtimeType);
			case 1: return Tuple2('secondarykey', secondarykey.runtimeType);
			case 2: return Tuple2('IntField1', IntField1.runtimeType);
			case 3: return Tuple2('StringField2', StringField2.runtimeType);
			case 4: return Tuple2('FloatField3', FloatField3.runtimeType);
			case 5: return Tuple2('EnumField4', EnumField4.runtimeType);
		}
		return null;
	}

	@override
	bool setPropertyValueFromName<T>(String propertyName, T value) {
		if (propertyName.toLowerCase() == 'primarykey') {
			if (checkPropertyType(primarykey, value) == false) {
				 return false;
			}
		
			primarykey = value as TestEnum;
			return true;
		}
		if (propertyName.toLowerCase() == 'secondarykey') {
			if (checkPropertyType(secondarykey, value) == false) {
				 return false;
			}
		
			secondarykey = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'intfield1') {
			if (checkPropertyType(IntField1, value) == false) {
				 return false;
			}
		
			IntField1 = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'stringfield2') {
			if (checkPropertyType(StringField2, value) == false) {
				 return false;
			}
		
			StringField2 = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'floatfield3') {
			if (checkPropertyType(FloatField3, value) == false) {
				 return false;
			}
		
			FloatField3 = value as double;
			return true;
		}
		if (propertyName.toLowerCase() == 'enumfield4') {
			if (checkPropertyType(EnumField4, value) == false) {
				 return false;
			}
		
			EnumField4 = value as TestEnum;
			return true;
		}
		return false;
	}
}
class TblCustomer extends TblBase
{
	int _primarykey= 0;
	int get primarykey => _primarykey;
	set primarykey(int value) {
		_primarykey = value;
		convertKey(_primarykey, true);
	}
	String name = '';
	String description = '';
	CustomerType type = CustomerType.none;
	String resource = '';
	int movespeed = 100;
	int get_probability = 0;
	CustomerSkillType skill_type = CustomerSkillType.none;
	int skill_probability = 0;
	int skill_value = 0;
	int need_rate = 0;
	int need_facility = 0;
	int need_topping = 0;
	int order_topping = 0;
	bool enable_share = false;

	@override
	int get propertiesCount => 15;
	@override
	Tuple2<String, Type> getPropertyInfo(int index) {
		switch (index) {
			case 0: return Tuple2('primarykey', primarykey.runtimeType);
			case 1: return Tuple2('name', name.runtimeType);
			case 2: return Tuple2('description', description.runtimeType);
			case 3: return Tuple2('type', type.runtimeType);
			case 4: return Tuple2('resource', resource.runtimeType);
			case 5: return Tuple2('movespeed', movespeed.runtimeType);
			case 6: return Tuple2('get_probability', get_probability.runtimeType);
			case 7: return Tuple2('skill_type', skill_type.runtimeType);
			case 8: return Tuple2('skill_probability', skill_probability.runtimeType);
			case 9: return Tuple2('skill_value', skill_value.runtimeType);
			case 10: return Tuple2('need_rate', need_rate.runtimeType);
			case 11: return Tuple2('need_facility', need_facility.runtimeType);
			case 12: return Tuple2('need_topping', need_topping.runtimeType);
			case 13: return Tuple2('order_topping', order_topping.runtimeType);
			case 14: return Tuple2('enable_share', enable_share.runtimeType);
		}
		return null;
	}

	@override
	bool setPropertyValueFromName<T>(String propertyName, T value) {
		if (propertyName.toLowerCase() == 'primarykey') {
			if (checkPropertyType(primarykey, value) == false) {
				 return false;
			}
		
			primarykey = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'name') {
			if (checkPropertyType(name, value) == false) {
				 return false;
			}
		
			name = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'description') {
			if (checkPropertyType(description, value) == false) {
				 return false;
			}
		
			description = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'type') {
			if (checkPropertyType(type, value) == false) {
				 return false;
			}
		
			type = value as CustomerType;
			return true;
		}
		if (propertyName.toLowerCase() == 'resource') {
			if (checkPropertyType(resource, value) == false) {
				 return false;
			}
		
			resource = value as String;
			return true;
		}
		if (propertyName.toLowerCase() == 'movespeed') {
			if (checkPropertyType(movespeed, value) == false) {
				 return false;
			}
		
			movespeed = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'get_probability') {
			if (checkPropertyType(get_probability, value) == false) {
				 return false;
			}
		
			get_probability = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'skill_type') {
			if (checkPropertyType(skill_type, value) == false) {
				 return false;
			}
		
			skill_type = value as CustomerSkillType;
			return true;
		}
		if (propertyName.toLowerCase() == 'skill_probability') {
			if (checkPropertyType(skill_probability, value) == false) {
				 return false;
			}
		
			skill_probability = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'skill_value') {
			if (checkPropertyType(skill_value, value) == false) {
				 return false;
			}
		
			skill_value = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'need_rate') {
			if (checkPropertyType(need_rate, value) == false) {
				 return false;
			}
		
			need_rate = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'need_facility') {
			if (checkPropertyType(need_facility, value) == false) {
				 return false;
			}
		
			need_facility = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'need_topping') {
			if (checkPropertyType(need_topping, value) == false) {
				 return false;
			}
		
			need_topping = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'order_topping') {
			if (checkPropertyType(order_topping, value) == false) {
				 return false;
			}
		
			order_topping = value as int;
			return true;
		}
		if (propertyName.toLowerCase() == 'enable_share') {
			if (checkPropertyType(enable_share, value) == false) {
				 return false;
			}
		
			enable_share = value as bool;
			return true;
		}
		return false;
	}
}
