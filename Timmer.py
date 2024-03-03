import pygame
import cv2
import numpy
from tkinter import simpledialog, Tk, Label, Entry, Button

root = Tk()
root.config(background="#6495ED")

def get_time():
    hours = int(entry_hours.get())
    minutes = int(entry_minutes.get())
    seconds = int(entry_seconds.get())
    
    return hours, minutes, seconds

def show_input_dialog():
    global entry_hours, entry_minutes, entry_seconds
    
    root.title("Timer Input")
    root.geometry("600x250")
    Label(root, text="Enter Hours, Minutes and Seconds",font =("Arial",15), background="#6495ED").grid(row=0, column=1, pady=5)
    Label(root, text="Hours:",background="#6495ED",font =("Arial",12) ).grid(row=1, column=0, pady=5)
    Label(root, text="Minutes:",background="#6495ED",font =("Arial",12)).grid(row=2, column=0, pady=5)
    Label(root, text="Seconds:",background="#6495ED",font =("Arial",12)).grid(row=3, column=0, pady=5)

    # creating the input widgets
    entry_hours = Entry(root, width=15)
    entry_minutes = Entry(root, width=15)
    entry_seconds = Entry(root, width=15)
    #positioning
    entry_hours.grid(row=1, column=1, pady=0)
    entry_minutes.grid(row=2, column=1, pady=0)
    entry_seconds.grid(row=3, column=1, pady=0)

    submit_button = Button(root, text="Submit", command=get_and_close,width = 15,height= 2)
    submit_button.grid(row=4, column=1, columnspan=1, pady=5)

    root.mainloop()

def get_and_close():
    global hours, minutes, seconds
    hours, minutes, seconds = get_time()
    root.withdraw()
    run_timer()

def drawArcCv2(surf, color, center, radius, width, end_angle):
    circle_image = numpy.zeros((radius * 2 + 4, radius * 2 + 4, 4), dtype=numpy.uint8)
    circle_image = cv2.ellipse(circle_image, (radius + 2, radius + 2),
                               (radius - width // 2, radius - width // 2), 0, 0, end_angle, (*color, 255), width,
                               lineType=cv2.LINE_AA)
    circle_surface = pygame.image.frombuffer(circle_image.flatten(), (radius * 2 + 4, radius * 2 + 4), 'RGBA')
    surf.blit(circle_surface, circle_surface.get_rect(center=center), special_flags=pygame.BLEND_PREMULTIPLIED)

def run_timer():
    pygame.init()
    
    window_width, window_height = 500, 500                         
    window = pygame.display.set_mode((window_width, window_height)) #window dimensions
    
    pygame.display.set_caption("Timer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 60)  

    

    total_seconds = hours * 3600 + minutes * 60 + seconds
    counter = total_seconds
    text = font.render(format_time(counter), True, (0, 0, 0))  # Adjusted text rendering

    timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(timer_event, 1000)

    run = True
    while run and counter >= 0:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == timer_event:
                counter -= 1
                text = font.render(format_time(counter), True, (125, 249, 255))
                if counter == 0:
                    pygame.time.set_timer(timer_event, 0)

        window.fill((0, 0, 0))
        text_rect = text.get_rect(center=window.get_rect().center)
        window.blit(text, text_rect)

        # Calculate the angle based on the remaining counter value
        angle = 360 * (total_seconds - counter) / total_seconds

        #loading wheel
        drawArcCv2(window, (0, 128, 0), (window_width // 2, window_height // 2), 120, 20, angle)

        pygame.display.flip()

    pygame.quit()
    exit()


def format_time(seconds):
    # Format the remaining time as HH:MM:SS
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f'{hours:02d}:{minutes:02d}:{seconds:02d}'

show_input_dialog()
