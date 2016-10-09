#!/usr/bin/python

from display_i2c import i2c_lcd
import button_mapping
import xml.etree.ElementTree as ET
import time

main_screen = i2c_lcd(0x27, 1, 2, 1, 0, 4, 5, 6, 7, 3)
main_screen.backLightOn()
main_screen.clear()
main_screen.home()
main_screen.command(0x0C) #disables the cursor

#now we parse just one xml file
tree = ET.parse('gui.xml')
root = tree.getroot()

starting_screen = 'screen[@name=\''+root.get('start')+'\']'
screen = root.find(starting_screen)
prev_screen = None
pressed = button_mapping.button_map.get(-1)
top_list = 0
list_selected = 0

def change_screen(screen_name):
	main_screen.clear()
	top_list = 0
	list_selected = 0
	return root.find('screen[@name=\''+screen_name+'\']'), screen

while True:
	row = 0
	column = 0
	main_screen.home()
	list_next_screen = ''
	for element in screen:
		if element.tag == 'string':
			string = ''
			if element.get('type') == 'eval':
				string = eval(element.text)
			else:
				string = element.text
			textLength = len(element.text)
			if element.get('align') == 'right':
				column = 20 - textLength
			elif element.get('align') == 'center':
				column = 9 - textLength/2
			row = int(element.get('row'))
			main_screen.setPosition(column, row)
			main_screen.writeString(string)
		elif element.tag == 'command':
			exec(element.text)
		elif element.tag == 'list':
			#how do I make a list?
			cursor = element.get('cursor')
			row = int(element.get('row'))
			home_row = row
			height = int(element.get('height'))
			if list_selected >= height:
				top_list = list_selected - height +1
			else:
				top_list = 0
			for index in range(top_list, top_list+height):
				main_screen.setPosition(column, row)
				string = element[index].text
				string += ' '*(20-len(string))
				if index == list_selected:
					main_screen.writeString(cursor+string)
					list_next_screen = element[index].get('next')
				else:
					main_screen.writeString(' '+string)
				row += 1
	pressed = button_mapping.read_button()
	if pressed == 'BACK':
		screen = prev_screen
		main_screen.clear()
	