from app import marsh_mallow as ma

class UserSerializer(ma.Schema):
	class Meta:
		fields = ('id', 'name', 'photo_url', 'photo_name', 'email', 'created_at', 'updated_at', 'pay_date')