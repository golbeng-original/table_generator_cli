
public class TableMeta
{
    public string tableName { get; set; } = "";
    public string dbName { get; set; } = "";

    public string clientDbName { get; set; } = "";
}

public partial class TblBase
{
    public static long ConvertKey(object key)
    {
        if(key is int)
        {
            return (long)key;
        }
        else if(key is uint)
        {
            return (long)key;
        }
        else if(key is string)
        {
            return (long)key.GetHashCode();
        }
        else if(key.GetType().IsEnum == true)
        {
            return (long)Convert.ToInt32(key);
        }
    }
}

public partial class TblBase
{
	public long queryPrimaryKey { get; private set; } = 0;
	public long querySecondaryKey { get; private set; } = 0;

	public virtual int propertiesCount { get => 0; }

	public IEnumerable<string> properties
	{
		get
		{
			for (int i = 0; i < propertiesCount; i++)
			{
				var propertyInfo = GetPropertyInfo(i);
				if (propertyInfo == null)
					continue;

				yield return propertyInfo?.propertyName;
			}
		}
	}

	public override bool Equals(object obj)
	{
		return obj is TblBase @base &&
			queryPrimaryKey == @base.queryPrimaryKey &&
			querySecondaryKey == @base.querySecondaryKey;
	}

	public override int GetHashCode()
	{
		int hashCode = -281792184;
		hashCode = hashCode * -1521134295 + queryPrimaryKey.GetHashCode();
		hashCode = hashCode * -1521134295 + querySecondaryKey.GetHashCode();
		return hashCode;
	}

	public virtual (string propertyName, Type type)? GetPropertyInfo(int index)
	{
		return null;
	}

	public bool SetPropertyValue(int index, object value)
	{
		var propertyInfo = GetPropertyInfo(index);
		if (propertyInfo == null)
			return false;

		return SetPropertyValue(propertyInfo?.propertyName, value);
	}

	public virtual bool SetPropertyValue(string propertyName, object value)
	{
		return false;
	}

	protected bool CheckProprtyType<T>(T targetProperty, object value)
	{
		return typeof(T) == value.GetType() ? true : false;
	}

	protected void ConvertKey(int key, bool primaryKey)
	{
		if (primaryKey == true)
			queryPrimaryKey = TblBase.ConvertKey(key);
		else
			querySecondaryKey = TblBase.ConvertKey(key);
	}

	protected void ConvertKey(uint key, bool primaryKey)
	{
		if (primaryKey == true)
			queryPrimaryKey = TblBase.ConvertKey(key);
		else
			querySecondaryKey = TblBase.ConvertKey(key);
	}

	protected void ConvertKey(string key, bool primaryKey)
	{
		key = key != null ? key : "";

		if (primaryKey == true)
			queryPrimaryKey = TblBase.ConvertKey(key);
		else
			querySecondaryKey = TblBase.ConvertKey(key);
	}

	protected void ConvertKey<T>(T key, bool primaryKey) where T : Enum
	{
		if (primaryKey == true)
			queryPrimaryKey = TblBase.ConvertKey(key);
		else
			querySecondaryKey = TblBase.ConvertKey(key);
	}
}


public class TblTestTable1 : TblBase
{
    private uint _primarykey = 0;
    private uint _secondarykey = 0;

    public uint primarykey
    {
        get => _primarykey;
        set
        {
            _primarykey = value;
            ConvertKey(_primarykey, true);
        }
    }

    public uint secondarykey
    {
        get => _secondarykey;
        set
        {
            _secondarykey = value;
            ConvertKey(_secondarykey, false);
        }
    }

    public int id { get; set; } = 0;

    public string name { get; set; } = "";

    //
    public override int propertiesCount { get => 4; }

	public override (string propertyName, Type type)? GetPropertyInfo(int index)
	{
		switch(index)
        {
            case 0: return (nameof(primarykey), primarykey.GetType());
            case 1: return (nameof(secondarykey), secondarykey.GetType());
            case 2: return (nameof(id), id.GetType());
            case 3: return (nameof(name), name.GetType());
        }

        return null;
	}

    public override bool SetPropertyValue(string propertyName, object value)
    {
		if (propertyName.Equals("primarykey", StringComparison.OrdinalIgnoreCase))
		{
			if (CheckProprtyType(primarykey, (uint)value) == false)
				return false;

			primarykey = (uint)value;
			return true;
		}

		if (propertyName.Equals("secondarykey", StringComparison.OrdinalIgnoreCase))
		{
			if (CheckProprtyType(secondarykey, (uint)value) == false)
				return false;

			secondarykey = (uint)value;
			return true;
		}

		if (propertyName.Equals("id", StringComparison.OrdinalIgnoreCase))
		{
			if (CheckProprtyType(id, (int)value) == false)
				return false;

			id = (int)value;
			return true;
		}

		if (propertyName.Equals("name", StringComparison.OrdinalIgnoreCase))
		{
			if (CheckProprtyType(name, (string)value) == false)
				return false;

			name = (string)value;
			return true;
		}
    }
}