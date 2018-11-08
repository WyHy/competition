"""Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
# register all the viewset to url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from rest_framework_swagger.views import get_swagger_view

from Allocation import views as allocations
from Backend.extend.CustomRouter import MultipleEntranceRouter
from PathologyType import views as types
from Profile import views as profiles
from TIFF import views as images
from UserType import views as usertypes
from Label import views as labels
from Activity import views as activities

multipleEntranceRouter = MultipleEntranceRouter()
# 用户信息
multipleEntranceRouter.register(r'profiles', profiles.ViewSet)
# 新建用户信息
multipleEntranceRouter.register(r'users', profiles.AddUserSet)
# 病理图像信息
multipleEntranceRouter.register(r'images/questions', images.QuestionViewSet)
multipleEntranceRouter.register(r'images/progress', images.ProgressViewSet)
multipleEntranceRouter.register(r'images/results', images.ResultViewSet)
multipleEntranceRouter.register(r'images', images.ViewSet)
# 病理类型信息
multipleEntranceRouter.register(r'types', types.ViewSet)
# 用户类型信息
multipleEntranceRouter.register(r'usertypes', usertypes.ViewSet)
# 任务分配信息
multipleEntranceRouter.register(r'missions', allocations.ViewSet)
# 大图细胞标注信息
multipleEntranceRouter.register(r'labels', labels.CellViewSet)
# 大图截图信息
multipleEntranceRouter.register(r'screenshots', labels.ScreenShotViewSet)

# 竞猜信息
multipleEntranceRouter.register(r'activities', activities.ViewSet)

schema_view = get_swagger_view(title='Competition API')

urlpatterns = [
    url(r'^api/v1/admin/', admin.site.urls),
    url(r'^api/v1/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/v1/doc/', schema_view),
    url(r'^api/v1/', include(multipleEntranceRouter.urls)),
    url(r'^api/v1/auth_token/', obtain_jwt_token),
    url(r'^api/v1/refresh_jwt_token/', refresh_jwt_token),
]

urlpatterns += staticfiles_urlpatterns()
