using System;

namespace Generate
{
	public class TblPiadgoods : TblBase
	{
		private uint _primarykey= 0;
		public  uint primarykey
		{
			get => _primarykey;
			set
			{
				_primarykey = value;
				ConvertKey(_primarykey, true);
			}
		}
		public PaymentType paymentType { get; set; } = PaymentType.None;
		public uint quantity { get; set; } = 0;
		public string productID { get; set; } = "";
		public MoneyType goodtype1 { get; set; } = MoneyType.None;
		public uint goodquantity1 { get; set; } = 0;
		public uint goodbonusquantity1 { get; set; } = 0;
		public MoneyType goodtype2 { get; set; } = MoneyType.None;
		public uint goodquantity2 { get; set; } = 0;
		public uint goodbonusquantity2 { get; set; } = 0;
		public string paidgood_icon { get; set; } = "";
	
		public override int propertiesCount { get => 11; }
	
		public override (string propertyName, Type type)? GetPropertyInfo(int index)
		{
			switch (index)
			{
				case 0: return (nameof(primarykey), primarykey.GetType());
				case 1: return (nameof(paymentType), paymentType.GetType());
				case 2: return (nameof(quantity), quantity.GetType());
				case 3: return (nameof(productID), productID.GetType());
				case 4: return (nameof(goodtype1), goodtype1.GetType());
				case 5: return (nameof(goodquantity1), goodquantity1.GetType());
				case 6: return (nameof(goodbonusquantity1), goodbonusquantity1.GetType());
				case 7: return (nameof(goodtype2), goodtype2.GetType());
				case 8: return (nameof(goodquantity2), goodquantity2.GetType());
				case 9: return (nameof(goodbonusquantity2), goodbonusquantity2.GetType());
				case 10: return (nameof(paidgood_icon), paidgood_icon.GetType());
			}
			return null;
		}
	
		public override bool SetPropertyValue(string propertyName, object value)
		{
			if (propertyName.Equals("primarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(primarykey, (uint)value) == false)
					 return false;
					
				primarykey = (uint)value;
				return true;
			}
			if (propertyName.Equals("paymentType", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(paymentType, (PaymentType)value) == false)
					 return false;
					
				paymentType = (PaymentType)value;
				return true;
			}
			if (propertyName.Equals("quantity", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(quantity, (uint)value) == false)
					 return false;
					
				quantity = (uint)value;
				return true;
			}
			if (propertyName.Equals("productID", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(productID, (string)value) == false)
					 return false;
					
				productID = (string)value;
				return true;
			}
			if (propertyName.Equals("goodtype1", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(goodtype1, (MoneyType)value) == false)
					 return false;
					
				goodtype1 = (MoneyType)value;
				return true;
			}
			if (propertyName.Equals("goodquantity1", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(goodquantity1, (uint)value) == false)
					 return false;
					
				goodquantity1 = (uint)value;
				return true;
			}
			if (propertyName.Equals("goodbonusquantity1", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(goodbonusquantity1, (uint)value) == false)
					 return false;
					
				goodbonusquantity1 = (uint)value;
				return true;
			}
			if (propertyName.Equals("goodtype2", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(goodtype2, (MoneyType)value) == false)
					 return false;
					
				goodtype2 = (MoneyType)value;
				return true;
			}
			if (propertyName.Equals("goodquantity2", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(goodquantity2, (uint)value) == false)
					 return false;
					
				goodquantity2 = (uint)value;
				return true;
			}
			if (propertyName.Equals("goodbonusquantity2", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(goodbonusquantity2, (uint)value) == false)
					 return false;
					
				goodbonusquantity2 = (uint)value;
				return true;
			}
			if (propertyName.Equals("paidgood_icon", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(paidgood_icon, (string)value) == false)
					 return false;
					
				paidgood_icon = (string)value;
				return true;
			}
			return false;
		}
	}
	public class TblMoney : TblBase
	{
		private MoneyType _primarykey= MoneyType.None;
		public  MoneyType primarykey
		{
			get => _primarykey;
			set
			{
				_primarykey = value;
				ConvertKey(_primarykey, true);
			}
		}
		public string name { get; set; } = "";
		public int maxvalue { get; set; } = 0;
		public string money_icon { get; set; } = "";
	
		public override int propertiesCount { get => 4; }
	
		public override (string propertyName, Type type)? GetPropertyInfo(int index)
		{
			switch (index)
			{
				case 0: return (nameof(primarykey), primarykey.GetType());
				case 1: return (nameof(name), name.GetType());
				case 2: return (nameof(maxvalue), maxvalue.GetType());
				case 3: return (nameof(money_icon), money_icon.GetType());
			}
			return null;
		}
	
		public override bool SetPropertyValue(string propertyName, object value)
		{
			if (propertyName.Equals("primarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(primarykey, (MoneyType)value) == false)
					 return false;
					
				primarykey = (MoneyType)value;
				return true;
			}
			if (propertyName.Equals("name", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(name, (string)value) == false)
					 return false;
					
				name = (string)value;
				return true;
			}
			if (propertyName.Equals("maxvalue", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(maxvalue, (int)value) == false)
					 return false;
					
				maxvalue = (int)value;
				return true;
			}
			if (propertyName.Equals("money_icon", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(money_icon, (string)value) == false)
					 return false;
					
				money_icon = (string)value;
				return true;
			}
			return false;
		}
	}
	public class TblTopping : TblBase
	{
		private uint _primarykey= 0;
		public  uint primarykey
		{
			get => _primarykey;
			set
			{
				_primarykey = value;
				ConvertKey(_primarykey, true);
			}
		}
		private uint _secondarykey= 0;
		public  uint secondarykey
		{
			get => _secondarykey;
			set
			{
				_secondarykey = value;
				ConvertKey(_secondarykey, false);
			}
		}
		public string name { get; set; } = "";
		public string description { get; set; } = "";
		public string resource { get; set; } = "";
		public ToppingType type { get; set; } = ToppingType.None;
		public int open_rate_grade { get; set; } = 0;
		public int open_Price_grade { get; set; } = 0;
		public int get_rate_grade { get; set; } = 0;
		public int get_price_grade { get; set; } = 0;
	
		public override int propertiesCount { get => 10; }
	
		public override (string propertyName, Type type)? GetPropertyInfo(int index)
		{
			switch (index)
			{
				case 0: return (nameof(primarykey), primarykey.GetType());
				case 1: return (nameof(secondarykey), secondarykey.GetType());
				case 2: return (nameof(name), name.GetType());
				case 3: return (nameof(description), description.GetType());
				case 4: return (nameof(resource), resource.GetType());
				case 5: return (nameof(type), type.GetType());
				case 6: return (nameof(open_rate_grade), open_rate_grade.GetType());
				case 7: return (nameof(open_Price_grade), open_Price_grade.GetType());
				case 8: return (nameof(get_rate_grade), get_rate_grade.GetType());
				case 9: return (nameof(get_price_grade), get_price_grade.GetType());
			}
			return null;
		}
	
		public override bool SetPropertyValue(string propertyName, object value)
		{
			if (propertyName.Equals("primarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(primarykey, (uint)value) == false)
					 return false;
					
				primarykey = (uint)value;
				return true;
			}
			if (propertyName.Equals("secondarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(secondarykey, (uint)value) == false)
					 return false;
					
				secondarykey = (uint)value;
				return true;
			}
			if (propertyName.Equals("name", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(name, (string)value) == false)
					 return false;
					
				name = (string)value;
				return true;
			}
			if (propertyName.Equals("description", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(description, (string)value) == false)
					 return false;
					
				description = (string)value;
				return true;
			}
			if (propertyName.Equals("resource", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(resource, (string)value) == false)
					 return false;
					
				resource = (string)value;
				return true;
			}
			if (propertyName.Equals("type", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(type, (ToppingType)value) == false)
					 return false;
					
				type = (ToppingType)value;
				return true;
			}
			if (propertyName.Equals("open_rate_grade", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(open_rate_grade, (int)value) == false)
					 return false;
					
				open_rate_grade = (int)value;
				return true;
			}
			if (propertyName.Equals("open_Price_grade", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(open_Price_grade, (int)value) == false)
					 return false;
					
				open_Price_grade = (int)value;
				return true;
			}
			if (propertyName.Equals("get_rate_grade", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(get_rate_grade, (int)value) == false)
					 return false;
					
				get_rate_grade = (int)value;
				return true;
			}
			if (propertyName.Equals("get_price_grade", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(get_price_grade, (int)value) == false)
					 return false;
					
				get_price_grade = (int)value;
				return true;
			}
			return false;
		}
	}
	public class TblFacility : TblBase
	{
		private uint _primarykey= 0;
		public  uint primarykey
		{
			get => _primarykey;
			set
			{
				_primarykey = value;
				ConvertKey(_primarykey, true);
			}
		}
		private uint _secondarykey= 0;
		public  uint secondarykey
		{
			get => _secondarykey;
			set
			{
				_secondarykey = value;
				ConvertKey(_secondarykey, false);
			}
		}
		public string name { get; set; } = "";
		public string description { get; set; } = "";
		public string resource { get; set; } = "";
		public FacilityType facilitytype { get; set; } = FacilityType.None;
		public int get_rate { get; set; } = 0;
		public InstallEffectType get_type { get; set; } = InstallEffectType.None;
		public int get_value { get; set; } = 0;
		public NeedType need_type { get; set; } = NeedType.None;
		public int need_value { get; set; } = 0;
		public int need_money { get; set; } = 0;
		public int get_money { get; set; } = 0;
		public bool enable_insert { get; set; } = true;
	
		public override int propertiesCount { get => 14; }
	
		public override (string propertyName, Type type)? GetPropertyInfo(int index)
		{
			switch (index)
			{
				case 0: return (nameof(primarykey), primarykey.GetType());
				case 1: return (nameof(secondarykey), secondarykey.GetType());
				case 2: return (nameof(name), name.GetType());
				case 3: return (nameof(description), description.GetType());
				case 4: return (nameof(resource), resource.GetType());
				case 5: return (nameof(facilitytype), facilitytype.GetType());
				case 6: return (nameof(get_rate), get_rate.GetType());
				case 7: return (nameof(get_type), get_type.GetType());
				case 8: return (nameof(get_value), get_value.GetType());
				case 9: return (nameof(need_type), need_type.GetType());
				case 10: return (nameof(need_value), need_value.GetType());
				case 11: return (nameof(need_money), need_money.GetType());
				case 12: return (nameof(get_money), get_money.GetType());
				case 13: return (nameof(enable_insert), enable_insert.GetType());
			}
			return null;
		}
	
		public override bool SetPropertyValue(string propertyName, object value)
		{
			if (propertyName.Equals("primarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(primarykey, (uint)value) == false)
					 return false;
					
				primarykey = (uint)value;
				return true;
			}
			if (propertyName.Equals("secondarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(secondarykey, (uint)value) == false)
					 return false;
					
				secondarykey = (uint)value;
				return true;
			}
			if (propertyName.Equals("name", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(name, (string)value) == false)
					 return false;
					
				name = (string)value;
				return true;
			}
			if (propertyName.Equals("description", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(description, (string)value) == false)
					 return false;
					
				description = (string)value;
				return true;
			}
			if (propertyName.Equals("resource", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(resource, (string)value) == false)
					 return false;
					
				resource = (string)value;
				return true;
			}
			if (propertyName.Equals("facilitytype", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(facilitytype, (FacilityType)value) == false)
					 return false;
					
				facilitytype = (FacilityType)value;
				return true;
			}
			if (propertyName.Equals("get_rate", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(get_rate, (int)value) == false)
					 return false;
					
				get_rate = (int)value;
				return true;
			}
			if (propertyName.Equals("get_type", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(get_type, (InstallEffectType)value) == false)
					 return false;
					
				get_type = (InstallEffectType)value;
				return true;
			}
			if (propertyName.Equals("get_value", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(get_value, (int)value) == false)
					 return false;
					
				get_value = (int)value;
				return true;
			}
			if (propertyName.Equals("need_type", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(need_type, (NeedType)value) == false)
					 return false;
					
				need_type = (NeedType)value;
				return true;
			}
			if (propertyName.Equals("need_value", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(need_value, (int)value) == false)
					 return false;
					
				need_value = (int)value;
				return true;
			}
			if (propertyName.Equals("need_money", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(need_money, (int)value) == false)
					 return false;
					
				need_money = (int)value;
				return true;
			}
			if (propertyName.Equals("get_money", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(get_money, (int)value) == false)
					 return false;
					
				get_money = (int)value;
				return true;
			}
			if (propertyName.Equals("enable_insert", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(enable_insert, (bool)value) == false)
					 return false;
					
				enable_insert = (bool)value;
				return true;
			}
			return false;
		}
	}
	public class TblExample_table : TblBase
	{
		private TestEnum _primarykey= TestEnum.None;
		public  TestEnum primarykey
		{
			get => _primarykey;
			set
			{
				_primarykey = value;
				ConvertKey(_primarykey, true);
			}
		}
		private string _secondarykey= "";
		public  string secondarykey
		{
			get => _secondarykey;
			set
			{
				_secondarykey = value;
				ConvertKey(_secondarykey, false);
			}
		}
		public int IntField1 { get; set; } = 0;
		public string StringField2 { get; set; } = "";
		public float FloatField3 { get; set; } = 0;
		public TestEnum EnumField4 { get; set; } = TestEnum.None;
	
		public override int propertiesCount { get => 6; }
	
		public override (string propertyName, Type type)? GetPropertyInfo(int index)
		{
			switch (index)
			{
				case 0: return (nameof(primarykey), primarykey.GetType());
				case 1: return (nameof(secondarykey), secondarykey.GetType());
				case 2: return (nameof(IntField1), IntField1.GetType());
				case 3: return (nameof(StringField2), StringField2.GetType());
				case 4: return (nameof(FloatField3), FloatField3.GetType());
				case 5: return (nameof(EnumField4), EnumField4.GetType());
			}
			return null;
		}
	
		public override bool SetPropertyValue(string propertyName, object value)
		{
			if (propertyName.Equals("primarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(primarykey, (TestEnum)value) == false)
					 return false;
					
				primarykey = (TestEnum)value;
				return true;
			}
			if (propertyName.Equals("secondarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(secondarykey, (string)value) == false)
					 return false;
					
				secondarykey = (string)value;
				return true;
			}
			if (propertyName.Equals("IntField1", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(IntField1, (int)value) == false)
					 return false;
					
				IntField1 = (int)value;
				return true;
			}
			if (propertyName.Equals("StringField2", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(StringField2, (string)value) == false)
					 return false;
					
				StringField2 = (string)value;
				return true;
			}
			if (propertyName.Equals("FloatField3", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(FloatField3, (float)value) == false)
					 return false;
					
				FloatField3 = (float)value;
				return true;
			}
			if (propertyName.Equals("EnumField4", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(EnumField4, (TestEnum)value) == false)
					 return false;
					
				EnumField4 = (TestEnum)value;
				return true;
			}
			return false;
		}
	}
	public class TblCustomer : TblBase
	{
		private uint _primarykey= 0;
		public  uint primarykey
		{
			get => _primarykey;
			set
			{
				_primarykey = value;
				ConvertKey(_primarykey, true);
			}
		}
		public string name { get; set; } = "";
		public string description { get; set; } = "";
		public CustomerType type { get; set; } = CustomerType.None;
		public string resource { get; set; } = "";
		public int movespeed { get; set; } = 100;
		public int get_probability { get; set; } = 0;
		public CustomerSkillType skill_type { get; set; } = CustomerSkillType.None;
		public int skill_probability { get; set; } = 0;
		public int skill_value { get; set; } = 0;
		public int need_rate { get; set; } = 0;
		public int need_facility { get; set; } = 0;
		public int need_topping { get; set; } = 0;
		public int order_topping { get; set; } = 0;
		public bool enable_share { get; set; } = false;
	
		public override int propertiesCount { get => 15; }
	
		public override (string propertyName, Type type)? GetPropertyInfo(int index)
		{
			switch (index)
			{
				case 0: return (nameof(primarykey), primarykey.GetType());
				case 1: return (nameof(name), name.GetType());
				case 2: return (nameof(description), description.GetType());
				case 3: return (nameof(type), type.GetType());
				case 4: return (nameof(resource), resource.GetType());
				case 5: return (nameof(movespeed), movespeed.GetType());
				case 6: return (nameof(get_probability), get_probability.GetType());
				case 7: return (nameof(skill_type), skill_type.GetType());
				case 8: return (nameof(skill_probability), skill_probability.GetType());
				case 9: return (nameof(skill_value), skill_value.GetType());
				case 10: return (nameof(need_rate), need_rate.GetType());
				case 11: return (nameof(need_facility), need_facility.GetType());
				case 12: return (nameof(need_topping), need_topping.GetType());
				case 13: return (nameof(order_topping), order_topping.GetType());
				case 14: return (nameof(enable_share), enable_share.GetType());
			}
			return null;
		}
	
		public override bool SetPropertyValue(string propertyName, object value)
		{
			if (propertyName.Equals("primarykey", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(primarykey, (uint)value) == false)
					 return false;
					
				primarykey = (uint)value;
				return true;
			}
			if (propertyName.Equals("name", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(name, (string)value) == false)
					 return false;
					
				name = (string)value;
				return true;
			}
			if (propertyName.Equals("description", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(description, (string)value) == false)
					 return false;
					
				description = (string)value;
				return true;
			}
			if (propertyName.Equals("type", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(type, (CustomerType)value) == false)
					 return false;
					
				type = (CustomerType)value;
				return true;
			}
			if (propertyName.Equals("resource", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(resource, (string)value) == false)
					 return false;
					
				resource = (string)value;
				return true;
			}
			if (propertyName.Equals("movespeed", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(movespeed, (int)value) == false)
					 return false;
					
				movespeed = (int)value;
				return true;
			}
			if (propertyName.Equals("get_probability", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(get_probability, (int)value) == false)
					 return false;
					
				get_probability = (int)value;
				return true;
			}
			if (propertyName.Equals("skill_type", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(skill_type, (CustomerSkillType)value) == false)
					 return false;
					
				skill_type = (CustomerSkillType)value;
				return true;
			}
			if (propertyName.Equals("skill_probability", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(skill_probability, (int)value) == false)
					 return false;
					
				skill_probability = (int)value;
				return true;
			}
			if (propertyName.Equals("skill_value", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(skill_value, (int)value) == false)
					 return false;
					
				skill_value = (int)value;
				return true;
			}
			if (propertyName.Equals("need_rate", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(need_rate, (int)value) == false)
					 return false;
					
				need_rate = (int)value;
				return true;
			}
			if (propertyName.Equals("need_facility", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(need_facility, (int)value) == false)
					 return false;
					
				need_facility = (int)value;
				return true;
			}
			if (propertyName.Equals("need_topping", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(need_topping, (int)value) == false)
					 return false;
					
				need_topping = (int)value;
				return true;
			}
			if (propertyName.Equals("order_topping", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(order_topping, (int)value) == false)
					 return false;
					
				order_topping = (int)value;
				return true;
			}
			if (propertyName.Equals("enable_share", StringComparison.OrdinalIgnoreCase))
			{
				if (CheckPropertyType(enable_share, (bool)value) == false)
					 return false;
					
				enable_share = (bool)value;
				return true;
			}
			return false;
		}
	}
}
