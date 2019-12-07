import aquael

light = aquael.Light('192.168.15.230')
light.poweron('200200112')
time.sleep(5)
light.poweroff()