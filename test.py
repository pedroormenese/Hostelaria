list_of_things = [
    {1: "dada"},
    {3: "dada"},
    {2: "dada"},
    {4: "dada"}
]

result = []

for num, value in enumerate(list_of_things):
    for key, internal_value in value.items():
        result.append(internal_value)

print(result)