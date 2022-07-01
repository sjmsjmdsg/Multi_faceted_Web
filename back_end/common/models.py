from django.db import models

# Create your models here.


# 存储网站访问次数
# class ClickNums(models.Model):
#     # 字段：访问次数
#     clickNums = models.IntegerField()

# CVE
class CveInfo(models.Model):
    # id
    cveid = models.CharField(max_length=50, primary_key=True)
    desc = models.CharField(max_length=1000,null=True)
    product = models.CharField(max_length=100,null=True)
    version = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=50,null=True)
    component = models.CharField(max_length=50,null=True)
    root = models.CharField(max_length=200,null=True)
    vector = models.CharField(max_length=100,null=True)
    impact = models.CharField(max_length=500,null=True)
    title = models.CharField(max_length=50,null=True)
    remedy = models.CharField(max_length=500,null=True)
    cwe = models.CharField(max_length=100,null=True)
    capec = models.CharField(max_length=100,null=True)
    cvss_score = models.CharField(max_length=20,null=True)
    severity = models.CharField(max_length=20,null=True)
    access = models.CharField(max_length=20,null=True)
    interaction = models.CharField(max_length=50,null=True)
    auth = models.CharField(max_length=20,null=True)
    attack_complex = models.CharField(max_length=20,null=True)
    impact_confidence = models.CharField(max_length=20,null=True)
    impact_integer = models.CharField(max_length=20,null=True)
    impact_available = models.CharField(max_length=20,null=True)
    publish_date = models.CharField(max_length=20,null=True)
    exploit_signature = models.CharField(max_length=50,null=True)


#Cve add Highlite
class CveInfoPlus(models.Model):
    cveid = models.CharField(max_length=50,primary_key=True)
    desc = models.CharField(max_length=1000,null=True)
    product = models.CharField(max_length=100,null=True)
    version = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=50,null=True)
    component = models.CharField(max_length=50,null=True)
    root = models.CharField(max_length=200,null=True)
    vector = models.CharField(max_length=100,null=True)
    impact = models.CharField(max_length=500,null=True)
    title = models.CharField(max_length=50,null=True)
    remedy = models.CharField(max_length=500,null=True)
    cwe = models.CharField(max_length=100,null=True)
    capec = models.CharField(max_length=100,null=True)
    cvss_score = models.CharField(max_length=20,null=True)
    severity = models.CharField(max_length=20,null=True)
    access = models.CharField(max_length=20,null=True)
    interaction = models.CharField(max_length=50,null=True)
    auth = models.CharField(max_length=20,null=True)
    attack_complex = models.CharField(max_length=20,null=True)
    impact_confidence = models.CharField(max_length=20,null=True)
    impact_integer = models.CharField(max_length=20,null=True)
    impact_available = models.CharField(max_length=20,null=True)
    publish_date = models.CharField(max_length=20,null=True)
    exploit_signature = models.CharField(max_length=50,null=True)


# aspect cvss info
class AspectCvssInfo(models.Model):
    aspect_id=models.CharField(max_length=50, primary_key=True)
    score = models.CharField(max_length=200)
    severity = models.CharField(max_length=200)
    access = models.CharField(max_length=200)
    interaction = models.CharField(max_length=200)
    auth = models.CharField(max_length=200)
    attackcomplex = models.CharField(max_length=200)
    impactconfidence = models.CharField(max_length=200)
    impactinteger = models.CharField(max_length=200)
    impactavailable = models.CharField(max_length=200)
    publishdate = models.CharField(max_length=300)


# aspect multi info
class AspectMultiInfo(models.Model):
    aspect_1 = models.CharField(max_length=60)
    aspect_2 = models.CharField(max_length=60)
    co_appear_time = models.IntegerField()


class AspectMultiInfoNew(models.Model):
    aspect_1 = models.CharField(max_length=60)
    aspect_2_ori = models.CharField(max_length=60)
    aspect_2 = models.CharField(max_length=1000)
    co_appear_time = models.IntegerField()

# aspect compare
class AspectCompare(models.Model):
    cveid = models.CharField(max_length=50,primary_key=True)
    nvd_product = models.CharField(max_length=120, null=True)
    nvd_version = models.CharField(max_length=120, null=True)
    nvd_vultype = models.CharField(max_length=120, null=True)
    nvd_component = models.CharField(max_length=120, null=True)
    nvd_root = models.CharField(max_length=120, null=True)
    nvd_vector = models.CharField(max_length=120, null=True)
    nvd_impact = models.CharField(max_length=120, null=True)
    ibm_product = models.CharField(max_length=120, null=True)
    ibm_version = models.CharField(max_length=120, null=True)
    ibm_vultype = models.CharField(max_length=120, null=True)
    ibm_component = models.CharField(max_length=120, null=True)
    ibm_root = models.CharField(max_length=120, null=True)
    ibm_vector = models.CharField(max_length=120, null=True)
    ibm_vector = models.CharField(max_length=120, null=True)
    ibm_impact = models.CharField(max_length=120, null=True)
    openwall_product = models.CharField(max_length=120, null=True)
    openwall_version = models.CharField(max_length=120, null=True)
    openwall_vultype = models.CharField(max_length=120, null=True)
    openwall_component = models.CharField(max_length=120, null=True)
    openwall_root = models.CharField(max_length=120, null=True)
    openwall_vector = models.CharField(max_length=120, null=True)
    openwall_impact = models.CharField(max_length=120, null=True)
    exploitdb_product = models.CharField(max_length=120, null=True)
    exploitdb_version = models.CharField(max_length=120, null=True)
    exploitdb_vultype = models.CharField(max_length=120, null=True)
    exploitdb_component = models.CharField(max_length=120, null=True)
    exploitdb_root = models.CharField(max_length=120, null=True)
    exploitdb_vector = models.CharField(max_length=120, null=True)
    exploitdb_impact = models.CharField(max_length=120, null=True)

# database indicator
class DatabaseIndicator(models.Model):
    cveid = models.CharField(max_length=50, primary_key=True)
    # cveid = models.ForeignKey(CveInfoPlus, db_column='cveid', on_delete=models.CASCADE)
    nvd_link = models.CharField(max_length=100)
    ibm_link = models.CharField(max_length=100)
    openwall_link = models.CharField(max_length=100)
    exploitdb_link = models.CharField(max_length=100)


# 执行以下代码，可以在Django管理员界面查看注册后的数据表
from django.contrib import admin
# admin.site.register(ClickNums)
admin.site.register(CveInfo)
admin.site.register(AspectCvssInfo)
# admin.site.register(AspectCvssYear)
admin.site.register(AspectMultiInfo)
# admin.site.register(AspectTable)
# admin.site.register(AspectYear)
