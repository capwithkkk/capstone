from crawler import CategoryConverger

count = CategoryConverger.instance().converge(10)
print(str(count))