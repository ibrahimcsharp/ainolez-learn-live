# Django talks to MySQL through the "MySQLdb" module. mysqlclient provides it but must be
# compiled, which many cPanel hosts cannot do, so PyMySQL (pure Python) stands in for it.
try:
    import MySQLdb  # noqa: F401  (mysqlclient, if installed)
except ImportError:
    import pymysql

    pymysql.install_as_MySQLdb()
