# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Loglogin(models.Model):
    logid = models.AutoField(db_column='logID', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='userID')  # Field name made lowercase.
    datecreated = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'LogLogin'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(blank=True, null=True)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField(blank=True, null=True)
    is_active = models.IntegerField(blank=True, null=True)
    role = models.ForeignKey('Role', models.DO_NOTHING, db_column='role', blank=True, null=True)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    uptime = models.DateTimeField(blank=True, null=True)
    downtime = models.DateTimeField(blank=True, null=True)
    average = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'batch'


class Cctv(models.Model):
    cctv_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    iframe = models.CharField(max_length=199, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cctv'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Dryer(models.Model):
    dryer_id = models.AutoField(primary_key=True)
    site_id = models.IntegerField(blank=True, null=True)
    conveyor_id = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=255)
    flag = models.IntegerField(blank=True, null=True)
    datecreated = models.DateTimeField()
    data1 = models.IntegerField(blank=True, null=True)
    data2 = models.IntegerField(blank=True, null=True)
    distance1 = models.CharField(max_length=50, blank=True, null=True)
    distance2 = models.CharField(max_length=50, blank=True, null=True)
    estimate_weight = models.CharField(max_length=199, blank=True, null=True)
    sampling = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dryer'


class Elevator(models.Model):
    elevator_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    sensor_address = models.IntegerField()
    station_id = models.IntegerField()
    site_id = models.IntegerField()
    flag = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'elevator'


class Operator(models.Model):
    operator_id = models.AutoField(primary_key=True)
    operator_name = models.CharField(max_length=255)
    operator_address = models.CharField(max_length=255)
    datecreated = models.DateTimeField()
    created_by = models.IntegerField()
    date_modified = models.DateTimeField()
    modified_by = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'operator'


class Role(models.Model):
    name = models.CharField(max_length=255)
    level = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'role'


class Sens(models.Model):
    sensor_id = models.AutoField(primary_key=True)
    sensor_type = models.IntegerField()
    name = models.CharField(max_length=255)
    datecreated = models.DateTimeField()
    site_id = models.IntegerField()
    dryer_id = models.IntegerField()
    station_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sens'
