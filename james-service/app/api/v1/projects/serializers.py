from app import marsh_mallow as ma

class ProjectSerializer(ma.Schema):
	class Meta:
		fields = ('id', 'title', 'description', 
			'copyright', 'dedication', 'status_value', 'color', 
			'author', 'created_at', 'updated_at', 'thumbnail_url', 'thumbnail_name')

class ProjectIdSerializer(ma.Schema):
	class Meta:
		fields = ('id',)

class ProjectSettingsSerializer(ma.Schema):
	class Meta:
		fields = ('id', 'orientation_value', 'margin_top', 
			'margin_right', 'margin_bottom', 'margin_left')