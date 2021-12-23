import Snake

snk = Snake.Snake()
# snk.border_collisions = True
snk.loadimages()
snk.starting_screen()

while snk.notstart:
    snk.delay(60)
    snk.events()
    snk.start()

timer = 0
while snk.run:
    snk.delay(60)
    snk.events()

    if timer == 18:
        snk.loop()
        timer = 0
    
        snk.display()
        snk.disp_update()

    timer += 1
    # 60Hz refresh rate is only used to register button presses
    # The actual sake movement needs to be slower (5Hz in this case)

snk.exit()

print('Score: ', snk.len)