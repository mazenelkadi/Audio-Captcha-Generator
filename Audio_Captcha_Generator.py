# Importing AudioCaptcha class from captcha module
from captcha.audio import AudioCaptcha
from random import randint  # Importing randint for generating random numbers

audio = AudioCaptcha()  # Creating an instance of AudioCaptcha
num = randint(100000, 999999)  # Generating a random 6-digit number
# Generating audio captcha data for the random number
data = audio.generate(str(num))
# Writing the generated audio data to an MP3 file
audio.write(str(num), str(num)+'.mp3')
print(num)  # Printing the random number (CAPTCHA value)
