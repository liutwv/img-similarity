# img-similarity
### 图像相似度计算
#### 包括：
* 根据颜色直方图计算余弦相似度
    参考：
    * https://segmentfault.com/a/1190000018849195
    * http://www.ruanyifeng.com/blog/2013/03/similar_image_search_part_ii.html
* 根据hash值计算汉明距离及相似度
* 根据特征点匹配ORB算法计算相似度

---
## 接口调用：
接口见api.py


## 安装使用：
本地构建镜像并推送到私有库：

`./build.sh`

服务端通过docker-compose安装：

- 修改docker-compose.yml中的版本号
- `docker-compose stop img-similarity`
- `docker-compose rm img-similarity`
- `docker-compose up -d img-similarity`

docker-compose.yml中的写法：

```
  img-similarity:
    image: xxx/img-similarity:1.0
    container_name: img-similarity
    ports:
      - "5001:5001"
    volumes:
      - "/mnt/logs/similarity:/opt/logs"
```