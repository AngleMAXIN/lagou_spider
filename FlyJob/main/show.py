from  pyecharts import Bar
from  .data import GetData


def salary_show():
    g = GetData()
    g.salary()
    bar = Bar()
    print(g.salary_data)
    salary_name, salary_count = bar.cast(g.salary_data)
    print(bar.cast(g.salary))
    bar.add("salary Bar", salary_name, salary_count,
            xaxis_interval=0, xaxis_rotate=30, yaxis_rotate=30)
    return bar

