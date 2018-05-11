from crawler import CategoryConverger

#count = CategoryConverger.instance().converge(10)
count = CategoryConverger.instance().converge_chain("바디케어", "바디")
print(str(count))