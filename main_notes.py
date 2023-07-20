# Реализовать консольное приложение заметки, с сохранением, чтением,
# добавлением, редактированием и удалением заметок. Заметка должна
# содержать идентификатор, заголовок, тело заметки и дату/время создания или
# последнего изменения заметки. Сохранение заметок необходимо сделать в
# формате json или csv формат (разделение полей рекомендуется делать через
# точку с запятой). Реализацию пользовательского интерфейса студент может
# делать как ему удобнее, можно делать как параметры запуска программы
# (команда, данные), можно делать как запрос команды с консоли и
# последующим вводом данных, как-то ещё, на усмотрение студента
# 
# Приложение должно запускаться без ошибок, должно уметь сохранять данные
# в файл, уметь читать данные из файла, делать выборку по дате, выводить на
# экран выбранную запись, выводить на экран весь список записок, добавлять
# записку, редактировать ее и удалять.
# При чтении списка заметок реализовать фильтрацию по дате.


import datetime
import json


class Note:
  def __init__(
    self,
    id,
    date_created,
    title,
    content
  ):
    self.title = title
    self.content = content
    self.date_created = date_created
    self.id = id
  

  def set_title(self,title):
    self.title = title
  
  def set_content(self,content):
    self.content = content

  def set_date_created(self,date_created):
    self.date_created = date_created

  def to_json(self): # метод для сохранения объекта в файл json
      return {
          'id': self.id,
          'create_date':self.date_created,
          'title': self.title,
          'content': self.content
      }  

  def save(self, filename):
    with open(filename, 'w+', encoding='utf8') as file:  # файл для записи  
      file.write(json.dumps(self.to_json(), sort_keys=True, indent=4, ensure_ascii=False))
  
  def print_all(self):
    print(f'ID #{self.id}')
    print(f'ДАТА СОЗДАНИЯ: {self.date_created}')
    print(f'ЗАГОЛОВОК: {self.title}')
    print('-----------------')
    print(f'ТЕКСТ ЗАМЕТКИ: {self.content}')
    print('=================\n')
  
  def print_for_list(self):
    print(f'--> ID #{self.id} | СОЗДАНА: {self.date_created} | ЗАГОЛОВОК: {self.title[:10]}')
 
#-----------------------------------------------

#-----метод ГЛАВНОЕ МЕНЮ-----
def main_menu():
  print("\033c", end="")
  while True:
    print('1.Создать новую заметку')
    print('2.Работа с заметкой')
    print('3.Работа со списком заметок')
    print('0.Завершить работу')
  
    choice = input ('---> ')
    match choice.split():
      case ['0']: # выход
        break

      case ['1']: # Создать новую заметку
        create_note()
    
      case ['2']: # Работа с заметкой
        sub_menu_note()
      
      case ['3']: # Работа со списком заметок
        sub_menu_notelist()

      case _:
        print('! не корректный выбор, повторите ввод !')


#-----метод СОЗДАНИЕ НОВОЙ ЗАМЕТКИ-----
def create_note():
  notes = read_from_file()
  title_input = input('Введите заголовок заметки: ')
  content_input = input('Введите текст заметки: ')
  current_datetime=datetime.datetime.now()
  date_created = current_datetime.strftime("%d.%m.%Y %H:%M:%S")
  id = str(len(notes)+1)
  new_note = Note (id, date_created, title_input, content_input)
  notes.append(new_note)
  print(f'! заметка #{id} успешно создана !\n')
  write_list_to_file(notes)
  

#-----метод  ЧТЕНИЕ ИЗ ФАЙЛА-----
def read_from_file():
  with open('notes.json') as file:
      data = json.load(file)

  notes = []
  for note in data['notes']:
      title = note['title']
      content = note['content']
      id = note['id']
      create_date = note['create_date']
      note_object = Note(id=id, date_created=create_date, title=title, content=content)
      notes.append(note_object)
  return notes


#!!!!-----метод ЗАПИСИ В ФАЙЛ-----
def write_list_to_file(notes_to_write): #notes_to_write - список объектов Note
  notes_to_json = []
  for note in notes_to_write:
    notes_to_json.append(note.to_json())
  
  all_notes_dict = {}
  all_notes_dict['notes'] = notes_to_json
  with open('notes.json', 'w') as file:  # открываем файл для записи в файл
    json.dump(all_notes_dict, file,  # запись дополненного словаря
              sort_keys=False, indent=4, ensure_ascii=False)
  print('! список заметок обновлен !\n')


#-----метод ВЛОЖЕННОЕ МЕНЮ "РАБОТА СО ЗАМЕТКОЙ"-----
def sub_menu_note():
  print("\033c", end="")

  while True:
    print('1.Показать заметку')
    print('2.Редактировать заметку')
    print('3.Удалить заметку')
    print('0.Вернуться в главное меню')
  
    choice = input ('---> ')
    match choice.split():
      case ['0']: # выход
        break

      case ['1']: # показать заметку
        purpose = 'просмотра'
        notes = read_from_file()
        note_to_show = find_note(purpose, notes)
        if note_to_show != None:
          note_to_show.print_all()
    
      case ['2']: # Редактировать заметку
        purpose = 'редактирования'
        notes = read_from_file()
        note_to_edit = find_note(purpose, notes)
        if note_to_edit != None:
          edit_note(note_to_edit, notes)
      
      case ['3']: # Удалить заметку
        purpose = 'удаления'
        notes = read_from_file()
        note_to_del = find_note(purpose, notes)
        if note_to_del != None:
          print(f'! заметка {note_to_del.id} будет удалена !')
          note_to_del.print_all()
          print('! Подтверждаете удаление(1-да/0-нет)?')
          while True:
            choi = input('---> ')
            match choi.split():
              case ['1']:
                del_note(note_to_del, notes)
                break

              case ['0']:
                #print(f'! заметка #{note_to_edit.id} осталась без изменения!\n')
                break

              case _:
                print('! не корректный выбор, повторите ввод !\n')
        
      case _:
        print('! не корректный выбор, повторите ввод !\n')


#-----метод ПОИСК ЗАМЕТКИ"-----
def find_note(purpose, notes):
  note_num = input (f'Введите номер заметки для {purpose}: ')
  for note in notes:
    if note.id == note_num:
      return note  
  print(f'Заметка с #{note_num} отсутствует\n')


#-----метод РЕДАКТИРОВАНИЯ ЗАМЕТКИ"-----
def edit_note(note_to_edit, notes):
  print("\033c", end="")
  print(f'РЕДАКТИРОВАНИЕ ЗАМЕТКИ #{note_to_edit.id}:')
  note_to_edit.print_all()  #выводим заметку на экран
  title_edit = input(f'РЕДАКТИРОВАТЬ ЗАГОЛОВОК "{note_to_edit.title}": ')
  content_edit = input(f'РЕДАКТИРОВАНИЕ ТЕКСТА "{note_to_edit.content}": ')
  print('\nСохранить изменения (1-да/0-нет)?')
  while True:
    choi = input('---> ')
    match choi.split():
      case ['1']:
        index = notes.index(note_to_edit)
        notes.pop(index)
        note_to_edit.set_title(title_edit)
        note_to_edit.set_content(content_edit)
        current_datetime = datetime.datetime.now()
        note_to_edit.set_date_created (current_datetime.strftime("%d.%m.%Y %H:%M:%S"))
        notes.append(note_to_edit)
        print(f'! заметка #{note_to_edit.id} успешно сохранена !:\n')
        note_to_edit.print_all()
        write_list_to_file(notes)
        break

      case ['0']:
        print(f'! заметка #{note_to_edit.id} осталась без изменения!\n')
        break

      case _:
        print('! не корректный выбор, повторите ввод !\n')

    note_to_edit.print_all()


#-----метод УДАЛЕНИЯ ЗАМЕТКИ"-----
def del_note(note_to_del, notes):
  index = notes.index(note_to_del)
  notes.pop(index) 
  print(f'! заметка #{note_to_del.id} удалена !\n')
  write_list_to_file(notes)  #записываем обновленный список в файл


#-----метод ВЛОЖЕННОЕ МЕНЮ "РАБОТА СО СПИСКОМ ЗАМЕТОК"-----
def sub_menu_notelist():
  print("\033c", end="")
  notes = read_from_file() 

  while True:
    print('1.Список заметок')
    print('2.Выборка за период')
    print('3.Выборка на дату')
    print('0.Вернуться в главное меню')
  
    choice = input ('---> ')
    match choice.split():
      case ['0']: # выход
        break

      case ['1']: # Список заметок
        print("\033c", end="")
        print('Список всех заметок:')
        for note in notes:
          note.print_for_list()
        print(f'---конец списка : всего {len(notes)} заметок---\n')
    
      case ['2']: # Выборка за период
        sample_from_period(notes) # метод ВЫБОРКИ ОБЪЕКТОВ ЗА ПЕРИОД

      case ['3']: # Выборка по дате
        sample_from_date(notes) # метод ВЫБОРКИ ОБЪЕКТОВ НА ДАТУ

      case _:
        print('! не корректный выбор, повторите ввод !')


#-----метод ВЫБОРКА ЗА ПЕРИОД"-----
def sample_from_period(notes):
  print("\033c", end="")
  print('ВЫБОРКА ЗАМЕТОК ЗА ПЕРИОД')
  date_start = input('Введите дату начала периода: ')
  date_end = input('Введите дату окончания периода: ')
  format = '%d.%m.%Y'
  date_start_input = datetime.datetime.strptime(date_start, format)
  date_end_input = datetime.datetime.strptime(date_end, format)
  
  count = 0
  for note in notes:
    datetime_note = datetime.datetime.strptime(note.date_created[:10], format) #[:10] оставляем только дату (время отсекаем)
    if (datetime_note >= date_start_input and datetime_note <= date_end_input):
      note.print_for_list()
      count = count + 1

  print(f'----ПОИСК ЗАВЕРШЕН--НАЙДЕНО {count} заметок----\n')


#-----метод ВЫБОРКА ПО ДАТЕ"-----
def sample_from_date(notes):
  print("\033c", end="")
  print('ВЫБОРКА ЗАМЕТОК НА УКАЗАННУЮ ДАТУ:')
  date_str = input('Введите дату: ') 
  format = '%d.%m.%Y'
  date = datetime.datetime.strptime(date_str, format)
  count = 0
  for note in notes:
    datetime_note = datetime.datetime.strptime(note.date_created[:10], format)
    if (datetime_note == date):
      note.print_for_list()
      count = count + 1
  print(f'----ПОИСК ЗАВЕРШЕН---НА ДАТУ {date_str} НАЙДЕНО {count} заметок----\n')


#----ОСНОВНОЙ КОД ПРОГРАММЫ-----------
main_menu()
