"""Program describes cook book"""

def get_digit(input_string):
  """
  (string) -> int or None

  Function check string and converts to number

  """

  try:
    number = int(input_string)
    return number
  except ValueError:
    print("Вы ввели некорректное значение, необходимо ввести число.")

def read_recipes(file_name):
  """

  (string) -> {} or None

  Function executes read text file with recipes of dishes

  """
  ingridient = {}
  recipes = {}

  try:
    with open(file_name, 'r', encoding='utf8') as file:
      while True:
        dish_name = file.readline().strip()
        if len(dish_name) <= 0:
          break

        count_ingridients = int(file.readline().strip())

        # Read information about ingridient
        ingridients = []
        for quantity in range(0, count_ingridients):
          ingridient_info = [element.strip() for element in file.readline().split('|')]

          ingridient["ingridient_name"] = ingridient_info[0]
          ingridient["quantity"] = ingridient_info[1]
          ingridient["measure"] = ingridient_info[2]
          ingridients.append(ingridient.copy())

        file.readline()
        recipes[dish_name] = ingridients
    return recipes
  except (FileNotFoundError):
    print(f"Файл с именем \"{file_name}\" не найден.")

def main():
  """

  (None) -> None

  Main function describe main functionality

  """

  def get_shop_list_by_dishes(dishes, person_count):
    """

    (list[], int) -> {}

    Function returns list of ingridients which need for prepare dishs by count of persons

    """
    nonlocal recipes

    count_ingridient = {}
    shop_list = {}

    for dish in dishes:
      ingridients = list(recipes[dish])
      for ingridient in ingridients:
        ingridient_name = ingridient["ingridient_name"]
        quantity_for_persons = person_count * int(ingridient["quantity"])

        # If already exists this ingridient
        if ingridient_name in shop_list.keys():
          count_ingridient = shop_list[ingridient_name]
          count_ingridient["quantity"] = count_ingridient["quantity"] + quantity_for_persons
        else:
          count_ingridient["measure"] = ingridient["measure"]
          count_ingridient["quantity"] = quantity_for_persons
          shop_list[ingridient["ingridient_name"]] = count_ingridient.copy()

    return shop_list

  recipes = read_recipes("recipes.txt")
  if not recipes:
     return
  # print_recipes(recipes)

  # Making up inviting string
  counter = 0
  info_string = ""
  for dish_name in recipes.keys():
    counter += 1
    info_string = info_string + str(counter) + "=\"" + dish_name + "\" "

  # Input list of names of dishes
  while True:
    print(info_string)
    try:
      dish_numbers = set(int(dish) for dish in input(f"Введите номера блюд через запятую, для которых хотите составить список продуктов для закупки (Пример: 1,3): ").split(","))
    except ValueError:
      print("Введена некорректная информация. ")
      continue

    found_wrong = False
    for number in dish_numbers:
      if number <= 0 or number > len(recipes):
        found_wrong = True
        print("Один из номеров введен некорректно.")
        break

    if not found_wrong:
      # All checks done
      break

  # print(dish_numbers)
  dishes_names = list(recipes.keys())
  # print(dishes_names)
  dishes = []
  for i in dish_numbers:
    dish_name = dishes_names[i-1]
    dishes.append(dish_name)
  # print(dishes)
  # dishes = ['Запеченный картофель', 'Омлет', 'Фахитос']

  # Input count of persons
  while True:
    count_persons = get_digit(input("Введите количество персон: "))
    if count_persons == None:
      continue

    if count_persons > 0:
      break
    else:
      print("Количество персон должно быть положительным числом.")
  # print(count_persons)

  shop_list = get_shop_list_by_dishes(dishes, count_persons)
  print(f"Список продуктов для приготовления {', '.join(dishes)} на {count_persons} персон: ")
  for what_to_buy in shop_list.keys():
    print(f"{what_to_buy} {shop_list[what_to_buy]}")

# Point of enter to program
main()
