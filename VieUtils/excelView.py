import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from pandas import DataFrame
from rest_framework import viewsets, serializers, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer


class EXCELview(viewsets.ModelViewSet):
    excel_lookup = 'file'

    def check_excel_and_get(self, request: Request):

        # 检验请求体字段
        try:
            file: InMemoryUploadedFile = request.data.get(self.excel_lookup)
        except:
            raise serializers.ValidationError({'fields': f'请求体中是否包含了{self.excel_lookup}字段'})
        # 检验文件类型
        try:
            df = pd.read_excel(file)
        except:
            raise serializers.ValidationError({'format': '无法读取该文件，请查看文件类型是否为xlsx'})
        return df

    def check_excel_field(self, df: DataFrame):
        excel_fields = df.columns.tolist()
        serializer_field = list(self.get_serializer().fields.keys())
        if set(excel_fields) != set(serializer_field):
            raise serializers.ValidationError({'fields_': '表格字段与指定字段不符'})

    def add_by_Excel(self, request: Request, *args, **kwargs):
        # 检验并获取Excel文件数据
        df:DataFrame = self.check_excel_and_get(request)
        # 检验Excel文件字段
        self.check_excel_field(df)

        result = []
        # 遍历数据并添加Item

        for index, row in df.iterrows():

            serializer:ModelSerializer = self.get_serializer(data=row.to_dict())
            if serializer.is_valid():
                serializer.save()
            else:
                result.append(
                    {
                        'value': row.to_dict(),
                        'msg': '数据不合法，无法添加'
                    }
                )

        if result:
            return Response({'result': result},status=status.HTTP_201_CREATED)
        else:
            return Response({'msg': 'success'},status=status.HTTP_201_CREATED)
