# Mxonline
Mxonline / django2.0+py3.6+adminx


激活虚拟环境后 安装依赖

settings.py:设置自己的邮箱


修改：

venv\lib\site-packages\django\forms\widgets.py


 line114: +   if list_2 is None:
 
  
 line115: +          list_2 = []
 
  
 line116:     for path in reversed(list_2):
 
              ......
  
