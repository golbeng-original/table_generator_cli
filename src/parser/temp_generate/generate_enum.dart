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
enum CustomerType
{
	/// None
	none,
	/// 일반 손님
	normal,
	/// 방해 손님
	interruption,
	/// 이벤트 손님
	event,
}
enum CustomerSkillType
{
	/// None
	none,
	/// 재화 획득 증가(배수)
	currencymultiply,
	/// 평점 획득 증가(배수)
	scoremultiply,
}
enum ToppingType
{
	/// None
	none,
	/// 일반 토핑
	normal,
	/// 이벤트 토핑
	event,
}
enum FacilityType
{
	/// None
	none,
	/// 손님 테이블
	parctice,
	/// 단순 장식용
	interior,
	/// 토핑 접수대
	receipt,
	/// 토핑 만드는 기계
	maker,
	/// 쓰레기통
	wastebaket,
}
enum NeedType
{
	/// None
	none,
	/// 설치 필요한 평점
	needrate,
	/// 설치 필요한 오픈 토핑
	needtopping,
	/// 설치 필요한 오픈 손님
	needcustomer,
}
enum InstallEffectType
{
	/// None
	none,
	/// 설치 시 게임 머니 획득 증가
	getmoney,
	/// 설치 시 펑점 획득 2배 증가
	getrate,
	/// 설치 시 토핑 시간 단축(%)
	gettoppingup,
}
enum MoneyType
{
	/// None
	none,
	/// 게임 머니(쿠키)
	gamemoney,
	/// 캐시 머니(잼)
	cashmoney,
	/// 평점
	ratescore,
	/// 패스권
	passticket,
}
enum PaymentType
{
	/// None
	none,
	/// IOS 플랫폼에서 지불 금액 타입
	iosbilling,
	/// Android 플랫폼 지불 금액 타입
	androidbilling,
	/// 쿠키 지불
	gamemoney,
	/// 잼 지불
	cashmoney,
}

int getGenerateEnumIndex(dynamic value) {
	if (value is TestEnum) {
		return value.index;
	}
	if (value is TestEnum2) {
		return value.index;
	}
	if (value is CustomerType) {
		return value.index;
	}
	if (value is CustomerSkillType) {
		return value.index;
	}
	if (value is ToppingType) {
		return value.index;
	}
	if (value is FacilityType) {
		return value.index;
	}
	if (value is NeedType) {
		return value.index;
	}
	if (value is InstallEffectType) {
		return value.index;
	}
	if (value is MoneyType) {
		return value.index;
	}
	if (value is PaymentType) {
		return value.index;
	}
	return 0;
}
