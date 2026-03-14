import os

# Optionally use PyMySQL as MySQLdb wrapper when requested via env var
if os.environ.get('USE_PYMYSQL') == '1' or os.environ.get('MYSQL_DB'):
	try:
		import pymysql
		pymysql.install_as_MySQLdb()
	except Exception:
		# if PyMySQL isn't installed it's fine; manage.py commands will error when run
		pass

# Django project package
