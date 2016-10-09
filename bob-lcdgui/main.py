from display_i2c import i2c_lcd
from buttons import ButtonReader
import screen
import sys
sys.path.append('.') #this is the path relative to bob_init.sh
from common.sender import sender

if __name__ == '__main__':
	main_screen = i2c_lcd(0x27, 1, 2, 1, 0, 4, 5, 6, 7, 3)
	main_screen.backLightOn()
	main_screen.clear()
	main_screen.home()
	main_screen.command(0x0C) #disables the cursor
	
	idle = screen.IdleScreen(main_screen)
	currentScreen = idle
	
	br = ButtonReader()
	
	while True:
		alarms = sender.sendMessage('get alarms')
		if alarms != '{}' and type(currentScreen) is not screen.AlarmScreen:
			currentScreen = screen.AlarmScreen(main_screen, alarms)
		pressed = br.getButton()
		currentScreen = currentScreen.updateScreen(pressed)