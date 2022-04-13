from datetime import datetime, timedelta
from dateutil import parser
#
# time = datetime.now()
# last_7_days = time - timedelta(days=7)
# last_30_days = time - timedelta(days=30)
#
# print(last_7_days.isoformat())
# print(time.isoformat())

date = "2020-08-29T00:00:00Z"
yourdate = parser.parse(date)
print(yourdate)

data = {
  "data": [
    {
      "lng": -122.51688114452725,
      "lat": 38.109947587584905,
      "timestamp_added": "2019-08-02T00:13:25.000000Z",
      "status": {
        "online": "online",
        "listen_addrs": ["/ip4/64.7.85.50/tcp/28762"],
        "height": 769399
      },
      "reward_scale": 1,
      "owner": "13fTdByCpUDRKuVh4VZcUWh7rdehrh4UfjMdFt17ew4h93nD86s",
      "nonce": 9,
      "name": "agreeable-walnut-weasel",
      "location": "8c2830ab51653ff",
      "last_poc_challenge": 750521,
      "last_change_block": 750521,
      "geocode": {
        "short_street": "Lockton Ln",
        "short_state": "CA",
        "short_country": "US",
        "short_city": "Novato",
        "long_street": "Lockton Lane",
        "long_state": "California",
        "long_country": "United States",
        "long_city": "Novato",
        "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
      },
      "block_added": 3805,
      "block": 771120,
      "address": "11tWRj2Qhnn177iVYm3KUmbPdMyhRfeqHqk9kCyiR7y57hdG9JA"
    },
    {
      "lng": -122.55193831997157,
      "lat": 38.1204024903364,
      "timestamp_added": "2019-08-01T15:44:31.000000Z",
      "status": {
        "online": "online",
        "listen_addrs": ["/ip4/76.102.181.228/tcp/44159"],
        "height": 771118
      },
      "reward_scale": 1,
      "owner": "13buBykFQf5VaQtv7mWj2PBY9Lq4i1DeXhg7C4Vbu3ppzqqNkTH",
      "nonce": 7,
      "name": "magic-rainbow-wasp",
      "location": "8c2830aa2a63dff",
      "last_poc_challenge": 771079,
      "last_change_block": 771079,
      "geocode": {
        "short_street": "Morning Star Ct",
        "short_state": "CA",
        "short_country": "US",
        "short_city": "Novato",
        "long_street": "Morning Star Court",
        "long_state": "California",
        "long_country": "United States",
        "long_city": "Novato",
        "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
      },
      "block_added": 3301,
      "block": 771120,
      "address": "112aeWRZdyz61Y7EQeMbXwqERNMPnciDvsxyFmhz1UfA9hte4R4W"
    },
    {
      "lng": -122.52885074963571,
      "lat": 38.12129445739087,
      "timestamp_added": "1970-01-01T00:00:00.000000Z",
      "status": {
        "online": "online",
        "listen_addrs": ["/ip4/76.102.181.228/tcp/44158"],
        "height": 771115
      },
      "reward_scale": 0.5,
      "owner": "13buBykFQf5VaQtv7mWj2PBY9Lq4i1DeXhg7C4Vbu3ppzqqNkTH",
      "nonce": 0,
      "name": "curly-berry-coyote",
      "location": "8c2830aa2529dff",
      "last_poc_challenge": 771113,
      "last_change_block": 771113,
      "geocode": {
        "short_street": "Andale Ave",
        "short_state": "CA",
        "short_country": "US",
        "short_city": "Novato",
        "long_street": "Andale Avenue",
        "long_state": "California",
        "long_country": "United States",
        "long_city": "Novato",
        "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
      },
      "block_added": 1,
      "block": 771120,
      "address": "112Z6fYnkQa8VAyMWHoaZJVzrxbWPoJV2NCfdZmaNoG1pYxWdGwD"
    },
    {
      "lng": -122.52885074963571,
      "lat": 38.12129445739087,
      "timestamp_added": "1970-01-01T00:00:00.000000Z",
      "status": {
        "online": "online",
        "listen_addrs": ["/ip4/76.102.181.228/tcp/44160"],
        "height": 768806
      },
      "reward_scale": 0.5,
      "owner": "13buBykFQf5VaQtv7mWj2PBY9Lq4i1DeXhg7C4Vbu3ppzqqNkTH",
      "nonce": 0,
      "name": "immense-eggplant-stallion",
      "location": "8c2830aa2529dff",
      "last_poc_challenge": 768733,
      "last_change_block": 771071,
      "geocode": {
        "short_street": "Andale Ave",
        "short_state": "CA",
        "short_country": "US",
        "short_city": "Novato",
        "long_street": "Andale Avenue",
        "long_state": "California",
        "long_country": "United States",
        "long_city": "Novato",
        "city_id": "bm92YXRvY2FsaWZvcm5pYXVuaXRlZCBzdGF0ZXM"
      },
      "block_added": 1,
      "block": 771120,
      "address": "11VKaN7fEvDm6NaGhcZtNSU1KAQQmTSwuuJsYYEqzh8mSWkoEUd"
    }
  ]
}