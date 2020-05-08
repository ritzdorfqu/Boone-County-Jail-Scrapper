import peewee


db = peewee.SqliteDatabase(
    'detainees.db',
    pragmas={'forgein_keys': 1}
)


class Info(peewee.Model):
    height = peewee.CharField(null=True)
    weight = peewee.CharField(null=True)
    sex = peewee.CharField(null=True)
    eyes = peewee.CharField(null=True)
    hair = peewee.CharField(null=True)
    race = peewee.CharField(null=True)
    age = peewee.CharField(null=True)
    city = peewee.CharField(null=True)
    state = peewee.CharField(null=True)

    class Meta:
        database = db

class Charges(peewee.Model):
    case_number = peewee.CharField(null=True)
    charge_description = peewee.CharField(null=True)
    charge_status = peewee.CharField(null=True)
    bail_amount = peewee.CharField(null=True)
    bond_type = peewee.CharField(null=True)
    court_date = peewee.DateField(null=True)
    court_time = peewee.TimeField(null=True)
    court_jurisdiction = peewee.CharField(null=True)

    class Meta:
        database = db

db.connect()
db.create_tables([Info, Charges])
