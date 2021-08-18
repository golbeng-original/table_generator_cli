namespace Generate
{
	public enum TestEnum
	{
		None = 0,
		Value_1 = 1, /// comment Value_1
		Value_2 = 2, /// comment Value_2
	}
	public enum TestEnum2
	{
		None = 0, /// None
		XXX = 4, /// XXX Comment
		YYY = 5,
	}
	public enum CustomerType
	{
		None = 0, /// None
		Normal = 1, /// 일반 손님
		Interruption = 2, /// 방해 손님
		Event = 3, /// 이벤트 손님
	}
	public enum CustomerSkillType
	{
		None = 0, /// None
		CurrencyMultiply = 1, /// 재화 획득 증가(배수)
		ScoreMultiply = 2, /// 평점 획득 증가(배수)
	}
	public enum ToppingType
	{
		None = 0, /// None
		Normal = 1, /// 일반 토핑
		Event = 2, /// 이벤트 토핑
	}
	public enum FacilityType
	{
		None = 0, /// None
		Parctice = 1, /// 손님 테이블
		Interior = 2, /// 단순 장식용
		Receipt = 3, /// 토핑 접수대
		Maker = 4, /// 토핑 만드는 기계
		Wastebaket = 5, /// 쓰레기통
	}
	public enum NeedType
	{
		None = 0, /// None
		NeedRate = 1, /// 설치 필요한 평점
		NeedTopping = 2, /// 설치 필요한 오픈 토핑
		NeedCustomer = 3, /// 설치 필요한 오픈 손님
	}
	public enum InstallEffectType
	{
		None = 0, /// None
		GetMoney = 1, /// 설치 시 게임 머니 획득 증가
		GetRate = 2, /// 설치 시 펑점 획득 2배 증가
		GetToppingUp = 3, /// 설치 시 토핑 시간 단축(%)
	}
	public enum MoneyType
	{
		None = 0, /// None
		GameMoney = 1, /// 게임 머니(쿠키)
		CashMoney = 2, /// 캐시 머니(잼)
		RateScore = 3, /// 평점
		PassTicket = 4, /// 패스권
	}
	public enum PaymentType
	{
		None = 0, /// None
		IosBilling = 1, /// IOS 플랫폼에서 지불 금액 타입
		AndroidBilling = 2, /// Android 플랫폼 지불 금액 타입
		GameMoney = 3, /// 쿠키 지불
		CashMoney = 4, /// 잼 지불
	}
}
