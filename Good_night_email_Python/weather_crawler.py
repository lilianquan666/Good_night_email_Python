import requests
import json
import re
from pypinyin import lazy_pinyin, Style  # 需先安装：pip install pypinyin

def main():
    # 1. 请求官方城市数据 JS 文件
    js_url = "https://j.i8tq.com/weather2020/search/city.js"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print("正在获取全国城市数据...")
    res = requests.get(js_url, headers=headers)
    res.encoding = "utf-8"

    # 2. 提取 JSON 数据（去掉 JS 变量声明）
    js_text = res.text
    json_str = re.sub(r"^var city_data\s*=\s*", "", js_text).rstrip(";")
    city_data = json.loads(json_str)

    cities = []
    # 3. 遍历全国所有省份
    for province_name, cities_in_province in city_data.items():
        # 4. 遍历省份下的地级市
        for city_name, districts in cities_in_province.items():
            if districts:
                # 取该地级市第一个区/县的 AREAID（通常对应市区）
                first_district = next(iter(districts.values()))
                area_id = first_district["AREAID"]
                real_url = f"http://www.weather.com.cn/weather/{area_id}.shtml"
                
                # 自动生成城市拼音（如“北京”→“beijing”）
                pinyin = "".join(lazy_pinyin(city_name, style=Style.NORMAL))
                cities.append((pinyin, real_url))

    # 5. 输出结果（前10个示例）
    print("\n===== 爬取结果（前10个） =====")
    for pinyin, link in cities[:10]:
        print(f"('{pinyin}','{link}'),")

    # 6. 保存到文件
    with open("city_weather_list.json", "w", encoding="utf-8") as f:
        f.write("city_list = [\n")
        for p, u in cities:
            f.write(f"    ('{p}','{u}'),\n")
        f.write("]\n")

    print(f"\n✅ 爬取完成！共获取 {len(cities)} 个全国城市！")

if __name__ == '__main__':
    main()