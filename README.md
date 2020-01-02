## API

### Get Category

```
GET http://host/get_category
```

```json
# Response Example

{
  "amount": 5, 	# 种类数
  "body": [
    {
      "id": 1, 	# category id
      "items": 2, 	# items in category
      "name": "致同学"	# category name
    }, 
    {
      "id": 2, 
      "items": 2, 
      "name": "致同事"
    }, 
    {
      "id": 3, 
      "items": 1, 
      "name": "致老师"
    }, 
    {
      "id": 4, 
      "items": 0, 
      "name": "致长辈"
    }, 
    {
      "id": 5, 
      "items": 0, 
      "name": "致朋友"
    }
  ], 
  "status": "ok"
}

```

### Get Bless

```
GET http://host/get_bless?page=1&per_page=10&category_id=0
```

- page：当前页数，default = 1
- per_page：每页条数，default = 10
- category_id：种类ID，default = 0

Response

```json
{
  "items": 5, 	# item in the response
  "message": [
    {
      "body": "家庭顺，事业顺，诸事一帆风顺；工作顺，前程顺，明天一顺百顺；发展顺，天地顺，祖国风调雨顺；生活顺，时时顺，新年一切皆顺！ ", 
      "category": {
        "id": 1, 
        "name": "致同学"
      }, 
      "id": 1
    }, 
    {
      "body": "新的一年开始，祝好事接2连3，心情4季如春，生活5颜6色，7彩缤纷，偶尔8点小财，烦恼抛到9霄云外！请接受我全心全意的祝福。祝新年快乐！ ", 
      "category": {
        "id": 1, 
        "name": "致同学"
      }, 
      "id": 2
    }, 
    {
      "body": "恭喜发财，福到万家，喜庆时刻，欢乐无限，祝君快乐，新年吉祥，幸福如意，健康平安，心想事成，万事顺心！ ", 
      "category": {
        "id": 2, 
        "name": "致同事"
      }, 
      "id": 3
    }, 
    {
      "body": "惦记着往日的笑声，忆取那温馨的爱抚，愿我们所有的日子洋溢着欢欣的喜悦。春节快乐、年年如意！ ", 
      "category": {
        "id": 2, 
        "name": "致同事"
      }, 
      "id": 4
    }, 
    {
      "body": "冬至饺子夏至面，愿你开心有人念，除夕夜里心情好，开心快乐过大年，过完春节闹元宵，新年出门捡钱包，打开钱包一千万，千万开心每一天！ ", 
      "category": {
        "id": 3, 
        "name": "致老师"
      }, 
      "id": 5
    }
  ], 
  "page": 1, 
  "pages": 1, 
  "status": "ok"
}
```



### Add User

```
POST http://host/add_user?
```

- openid(必须)
- nickname(必须)
- gender
- city
- province
- country
- avatarurl
- unionid

```
# 成功
{
  "status": "created",
  "user": "openid_tianbybyvyv"
}

{
  "status": "updated",
  "user": "openid_tianbybyvyv"
}

# 失败
{
  "message": "openid and nickname required.",
  "status": "fail"
}
```

  

### Add Favourates to User

```
POST http://host/add_favourite
```

- user_id
- message_id



### Get User Favourates

```
GET http://host/get_user_collection/<user_id>
```







