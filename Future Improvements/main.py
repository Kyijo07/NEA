def main():
    components = {"Wire": "-", "Light Bulb OFF": "^", "Light Bulb ON": "*", "NOT Gate": "N", "AND GATE": "A",
                  "OR GATE": "O", "Switch Off": "_", "Switch On": "/"}

    sample_grid = [
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", "", ""]
    ]
    x = input("x: ")
    y = input("y: ")
    component = input("Component: ")
    for i in components:
        if component == i:
            sample_grid[x, y] = str(components[i])
        else:
            continue
    print(sample_grid)

main()
