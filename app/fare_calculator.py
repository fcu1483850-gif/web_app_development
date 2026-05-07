from .models import FareModel

def calculate_bus_fare(distance_km):
    """
    計算台中公車票價：雙十優惠
    前 10 公里免費 (0 元)
    超過 10 公里部分，最多收費 10 元
    （為簡化計算，我們假設基本費率為 0，超過 10km 後不論多遠皆收最高 10 元）
    """
    if distance_km <= 10:
        return 0
    else:
        return 10

def calculate_mrt_fare(start_station, end_station):
    """
    計算台中捷運票價：透過查詢 SQLite 費率表
    """
    if start_station == end_station:
        return 0
    
    fare = FareModel.get_mrt_fare(start_station, end_station)
    if fare is not None:
        return fare
    else:
        # 如果找不到對應的站點費率，回傳預設起步價 20 元
        return 20

def calculate_youbike_fare(minutes):
    """
    計算 YouBike 費率：
    預設為 2.0 費率計算方式
    前 30 分鐘 10 元 (或 0 元如有補助，此處以 0 元計)
    後續每 30 分鐘 10 元
    """
    if minutes <= 30:
        return 0
    elif minutes <= 4 * 60:
        # 超過 30 分鐘，但在 4 小時內，每 30 分鐘 10 元
        periods = (minutes - 1) // 30
        return periods * 10
    else:
        # 超過 4 小時部分（可依實際規則調整，這裡簡化計算）
        periods = (minutes - 1) // 30
        return periods * 10

def calculate_total_fare(transports):
    """
    計算總交通費用
    transports 是一個 list of dicts, 例如:
    [
        {"type": "bus", "distance_km": 15},
        {"type": "mrt", "start_station": "G0", "end_station": "G17"},
        {"type": "youbike", "minutes": 45}
    ]
    """
    total_cost = 0
    details = []

    for item in transports:
        t_type = item.get("type")
        cost = 0
        if t_type == "bus":
            distance = item.get("distance_km", 0)
            cost = calculate_bus_fare(distance)
        elif t_type == "mrt":
            start = item.get("start_station", "")
            end = item.get("end_station", "")
            cost = calculate_mrt_fare(start, end)
        elif t_type == "youbike":
            mins = item.get("minutes", 0)
            cost = calculate_youbike_fare(mins)
        else:
            # 未知的交通工具類型
            cost = 0

        total_cost += cost
        details.append({
            "type": t_type,
            "cost": cost
        })

    return {
        "status": "success",
        "details": details,
        "total_cost": total_cost
    }
