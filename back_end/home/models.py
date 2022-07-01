from django.db import models


# Create your models here.


class WebClickNums(models.Model):
    # 字段：访问次数
    clickNums = models.IntegerField()

class Aspect2CvssYear(models.Model):
    aspect_id = models.CharField(max_length=50, primary_key=True)
    y1980 = models.CharField(max_length=20, null=True)
    y1981 = models.CharField(max_length=20, null=True)
    y1982 = models.CharField(max_length=20, null=True)
    y1983 = models.CharField(max_length=20, null=True)
    y1984 = models.CharField(max_length=20, null=True)
    y1985 = models.CharField(max_length=20, null=True)
    y1986 = models.CharField(max_length=20, null=True)
    y1987 = models.CharField(max_length=20, null=True)
    y1988 = models.CharField(max_length=20, null=True)
    y1989 = models.CharField(max_length=20, null=True)
    y1990 = models.CharField(max_length=20, null=True)
    y1991 = models.CharField(max_length=20, null=True)
    y1992 = models.CharField(max_length=20, null=True)
    y1993 = models.CharField(max_length=20, null=True)
    y1994 = models.CharField(max_length=20, null=True)
    y1995 = models.CharField(max_length=20, null=True)
    y1996 = models.CharField(max_length=200, null=True)
    y1997 = models.CharField(max_length=200, null=True)
    y1998 = models.CharField(max_length=200, null=True)
    y1999 = models.CharField(max_length=200, null=True)
    y2000 = models.CharField(max_length=200, null=True)
    y2001 = models.CharField(max_length=200, null=True)
    y2002 = models.CharField(max_length=200, null=True)
    y2003 = models.CharField(max_length=200, null=True)
    y2004 = models.CharField(max_length=200, null=True)
    y2005 = models.CharField(max_length=200, null=True)
    y2006 = models.CharField(max_length=200, null=True)
    y2007 = models.CharField(max_length=200, null=True)
    y2008 = models.CharField(max_length=200, null=True)
    y2009 = models.CharField(max_length=200, null=True)
    y2010 = models.CharField(max_length=200, null=True)
    y2011 = models.CharField(max_length=200, null=True)
    y2012 = models.CharField(max_length=300, null=True)
    y2013 = models.CharField(max_length=300, null=True)
    y2014 = models.CharField(max_length=300, null=True)
    y2015 = models.CharField(max_length=300, null=True)
    y2016 = models.CharField(max_length=300, null=True)
    y2017 = models.CharField(max_length=300, null=True)
    y2018 = models.CharField(max_length=300, null=True)
    y2019 = models.CharField(max_length=300, null=True)
    y2020 = models.CharField(max_length=300, null=True)
    y2021 = models.CharField(max_length=300, null=True)

class Aspect2Year(models.Model):
    aspect_id = models.CharField(max_length=50, primary_key=True)
    y1980 = models.IntegerField()
    y1981 = models.IntegerField()
    y1982 = models.IntegerField()
    y1983 = models.IntegerField()
    y1984 = models.IntegerField()
    y1985 = models.IntegerField()
    y1986 = models.IntegerField()
    y1987 = models.IntegerField()
    y1988 = models.IntegerField()
    y1989 = models.IntegerField()
    y1990 = models.IntegerField()
    y1991 = models.IntegerField()
    y1992 = models.IntegerField()
    y1993 = models.IntegerField()
    y1994 = models.IntegerField()
    y1995 = models.IntegerField()
    y1996 = models.IntegerField()
    y1997 = models.IntegerField()
    y1998 = models.IntegerField()
    y1999 = models.IntegerField()
    y2000 = models.IntegerField()
    y2001 = models.IntegerField()
    y2002 = models.IntegerField()
    y2003 = models.IntegerField()
    y2004 = models.IntegerField()
    y2005 = models.IntegerField()
    y2006 = models.IntegerField()
    y2007 = models.IntegerField()
    y2008 = models.IntegerField()
    y2009 = models.IntegerField()
    y2010 = models.IntegerField()
    y2011 = models.IntegerField()
    y2012 = models.IntegerField()
    y2013 = models.IntegerField()
    y2014 = models.IntegerField()
    y2015 = models.IntegerField()
    y2016 = models.IntegerField()
    y2017 = models.IntegerField()
    y2018 = models.IntegerField()
    y2019 = models.IntegerField()
    y2020 = models.IntegerField()
    y2021 = models.IntegerField()

class Aspect2Table(models.Model):
    aspect_id = models.CharField(max_length=50)
    aspect = models.CharField(max_length=200, primary_key=True)

class Aspect2TableNew(models.Model):
    aspect_id = models.CharField(max_length=50)
    aspect_ori = models.CharField(max_length=200, null=True)
    aspect = models.CharField(max_length=1000, null=True)

class WordThesaurus(models.Model): #该cvs文件没有表头
    thesaurus = models.CharField(max_length=50,null=True)
    type = models.CharField(max_length=50, null=True)

class WordType2(models.Model): #该cvs文件没有表头
    word = models.CharField(max_length=50,null=True)
    type = models.CharField(max_length=50, null=True)

class Phrase2Cve(models.Model): #该cvs文件没有表头
    word = models.CharField(max_length=100,null=True)
    type = models.CharField(max_length=50, null=True)

class Word2Cve(models.Model): #该cvs文件没有表头
    word = models.CharField(max_length=50, null=True)
    type = models.CharField(max_length=50, null=True)

# 执行以下代码，可以在Django管理员界面查看注册后的数据表
from django.contrib import admin
admin.site.register(WebClickNums)