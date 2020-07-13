from pyecharts.datasets import register_url

from pyecharts import options as opts
from pyecharts.charts import Geo
from pyecharts.faker import Faker
from pyecharts.globals import ChartType
import pandas as pd
from pyecharts.charts import Timeline
import datetime
import matplotlib.pyplot as plt


# 韩国疫情图
def heat(l_pos, l_confirmed):
    g = Geo().add_schema(maptype="韩国")
    for (name, latitude, longitude) in l_pos:
        g = g.add_coordinate(name=name, latitude=latitude, longitude=longitude)
    for (name, num) in l_confirmed:
        g = g.add(name + ": " + str(num), [(name, num)], type_=ChartType.HEATMAP, )
    c = (
        g.set_series_opts(label_opts=opts.LabelOpts(is_show=True, formatter="{b}: {c}"),
                          position='bottom').set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="韩国疫情图"),
            legend_opts=opts.LegendOpts(type_="scroll", pos_right="right", orient="vertical"),
        ).render("韩国疫情图.html")
    )
    print(c)


# 韩国疫情随时间变化图
def time_change(l_pos):
    df_time = pd.read_csv("./TimeProvince.csv")
    tl = Timeline()
    cur_day = datetime.datetime(year=2020, month=1, day=20)
    for i in range(0, len(df_time), 170):
        g = Geo().add_schema(maptype="韩国")
        for (name, latitude, longitude) in l_pos:
            g = g.add_coordinate(name=name, latitude=latitude, longitude=longitude)
        df_day = df_time[i:i + 17]
        df_day = df_day[["province", "confirmed"]]
        l_day = df_day.values.tolist()
        for (name, num) in l_day:
            g = g.add(name + ": " + str(num), [(name, num)], type_=ChartType.HEATMAP, )
        c = (
            g.set_series_opts(label_opts=opts.LabelOpts(is_show=True, ),
                              position='bottom').set_global_opts(
                visualmap_opts=opts.VisualMapOpts(),
                title_opts=opts.TitleOpts(title="自2020.1.20日起,韩国疫情变化图", subtitle="每10日一统计,数据来源实验表格"),
                legend_opts=opts.LegendOpts(type_="scroll", pos_right="right", orient="vertical"),
            )
        )
        del g
        tl.add(c, cur_day.strftime("%Y-%m-%d"))
        cur_day = cur_day + datetime.timedelta(days=10)
    tl.render("韩国疫情随时间变化图.html")
    print(tl)


# 获取位置信息与传染病信息
def read_scv():
    df_pos = pd.read_csv("./Region.csv")
    df_pos = df_pos[["province", "latitude", "longitude"]]
    # print(df_pos)
    l_pos = df_pos.values.tolist()
    df_case = pd.read_csv("./Case.csv")
    confirmed = df_case.groupby("province")["confirmed"].sum()
    l_confirmed = confirmed.reset_index().values.tolist()
    return l_pos, l_confirmed


# 可视化
def visualization():
    df = pd.read_csv("./PatientInfo.csv")
    cols = ["sex", "age", "country", "infection_case"]
    for c in cols:
        df_temp = df[c]
        # print(df_sex)
        if c == "age":
            df_temp.value_counts().plot.pie()
        else:
            df_temp.value_counts().plot.bar()
        # by_sex = df_sex.groupby("sex")["sex"].count()
        # p = by_sex.plot().bar()
        # print(by_sex)
        plt.title("by_" + c)
        plt.savefig("./by_" + c + ".png")
        plt.close()

    df_p = df[df["country"] == "Korea"]["province"]
    df_p.value_counts().plot.bar()
    plt.title("by_" + "Korea_province")
    plt.savefig("./by_" + "Korea_province" + ".png")
    plt.close()


def ml():
    df_time = pd.read_csv("./TimeProvince.csv")
    sum_confirmed = df_time.groupby("date")["confirmed"].sum()
    sum_released = df_time.groupby("date")["released"].sum()
    sum_deceased = df_time.groupby("date")["deceased"].sum()
    print(sum_num)


def sir():
    import scipy.integrate
    import numpy as np

    # model
    def SIR_model(y, t, beta, gamma):
        S, I, R = y
        dS_dt = -beta * S * I
        dI_dt = beta * S * I - gamma * I
        dR_dt = gamma * I
        return ([dS_dt, dI_dt, dR_dt])

    # initialization

    S0 = 0.9  # ratio
    I0 = 0.1  # ratio
    R0 = 0.0  # ratio
    beta = 0.35
    gamma = 0.1

    # time vector
    t = np.linspace(0, 100, 10000)
    # result
    res = scipy.integrate.odeint(SIR_model, [S0, I0, R0], t, args=(beta, gamma))
    res = np.array(res)
    # plot
    plt.figure(figsize=[6, 4])
    plt.plot(t, res[:, 0], label='S(t)')
    plt.plot(t, res[:, 1], label='I(t)')
    plt.plot(t, res[:, 2], label='R(t)')
    plt.legend()
    plt.grid()
    plt.xlabel('time')
    plt.ylabel('proportions')
    plt.title('SIR model simulation')
    plt.show()


if __name__ == '__main__':
    # l_pos, l_confirmed = read_scv()
    # time_change(l_pos)
    # heat(l_pos, l_confirmed)
    # visualization()
    ml()
