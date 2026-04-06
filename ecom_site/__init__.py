import os

# If PyMySQL is installed, register it as MySQLdb so Django's MySQL
# backend can load without the native mysqlclient package.
try:
	import pymysql
	pymysql.install_as_MySQLdb()
except Exception:
	# Leave silently if PyMySQL is not available; the runtime will raise
	# the original ImportError which is helpful for debugging.
	pass

# Django project package
