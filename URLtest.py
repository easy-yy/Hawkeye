import requests

if __name__ == '__main__':
    path = 'http://172.23.252.215:8333'

    # 获取文件列表
    # url = '/DataManagementSystem/selectAll'
    # res = requests.post(
    #     url=path + url
    # )
    # print(res.json())

    # 下载图片
    # 1. 原图  2. 预处理图片 3. 分割图像 4. 识别结果图像 5. 样本标注图像 6. 鉴定结果
    # url = '/DataManagementSystem/download'
    # data = {
    #     'fileName': 'BZ282S1015-5X-A-1.jpg',
    #     'typeId': 1
    # }
    # res = requests.get(url=path+url, params=data)
    # with open('./out/BZ282S1015-5X-A-1.jpg', 'wb') as f:
    #     f.write(res.content)


    # 文件上传
    url = '/DataManagementSystem/OriPicAdd'

    # 单文件
    files = {
        'file': open('re1/324-1.jpg', 'rb'),
    }
    data = {
        'typeId': 1,
    }
    res = requests.post(
        url=path+url,
        data=data,
        files=files
    )
    print(res.json())

    # 判断文件是否存在
    # url = '/DataManagementSystem/isExit'
    # res = requests.post(
    #     url=path+url,
    #     data={
    #         'fileName': 'CCCCCC',
    #         'typeId': 1
    #     }
    # )
    # print(res.json())

    #
    # url = '/DataManagementSystem/selectByViFiId'
    # res = requests.post(
    #     url=path+url,
    #     data={
    #         'key': '20210316030837936'
    #     }
    # )
    # print(res.json())

    # url = '/DataManagementSystem/selectByStatus'
    # res = requests.post(
    #     url=path+url,
    #     data={
    #         'typeName': 1
    #     }
    # )
    # print(res.json())



# import os
# import urllib.request
# import requests
#
# from urllib3 import encode_multipart_formdata
#
# image_url = 'http://172.23.252.215:8333/image/'
# file_path = 'FWQ/'
# keyword = "原始图像"
# key = urllib.request.quote(keyword)
# URL = image_url + key + '/'
#
#
# def downloadImage():
#     url = URL + 'BZ282S1015-5X-A-1.JPG'
#     # print(url)
#     try:
#         if not os.path.exists(file_path):
#             os.makedirs(file_path)
#         filename = 'FWQ/BZ282S1015-5X-A-1.JPG'
#         urllib.request.urlretrieve(url, filename=filename)
#         print('下载成功！')
#     except IOError as e:
#         print(1, e)
#     except Exception as e:
#         print(2, e)
#
#
# def uploadImage():
#     url = "http://172.23.252.215:8333/DataManagementSystem/OriPicAdd"  # 请求的接口地址
#     pass
#
#
# if __name__ == '__main__':
#     uploadImage()
