import datetime
from datetime import timedelta

data_atual = datetime.datetime.now()
data_futura = data_atual + timedelta(days=30)
print(f"Data atual: {data_atual}")
print(f"Data futura: {data_futura}")
