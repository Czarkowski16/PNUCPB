import pygame
import time

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH, SCREEN_HEIGHT = 1220, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wywiad z animatronem")

# Ładowanie zasobów
tlo1 = pygame.image.load("1.png")
przycisk_gora = pygame.image.load("góra.png")
notatnik = pygame.image.load("papier.png")

# Czcionka
font = pygame.font.Font(None, 30)
small_font = pygame.font.Font(None, 30)

# Tekst pytania
pytanie_text = font.render("Czy robot zareagował na dźwięk?", True, (0, 0, 0))



# Lista przycisków odpowiedzi
odpowiedzi = []
start_y = 200
for i in range(4):
    tak_rect = pygame.Rect(600, start_y + i * 60, 20, 20)  # Jeszcze bardziej w prawo
    nie_rect = pygame.Rect(700, start_y + i * 60, 20, 20)  # Jeszcze bardziej w prawo
    odpowiedzi.append({"tak": tak_rect, "nie": nie_rect, "tak_selected": False, "nie_selected": False})

# Dźwięki
dzwiek_wywiad = pygame.mixer.Sound("cassete man.mp3")
dzwiek_czarek = pygame.mixer.Sound("Czarek.mp3")

# Skalowanie przycisków i notatnika
przycisk_gora = pygame.transform.scale(przycisk_gora, (przycisk_gora.get_width() // 2, przycisk_gora.get_height() // 2))
notatnik = pygame.transform.scale(notatnik, (notatnik.get_width() * 1.2, notatnik.get_height() * 1.2))

# Pozycje przycisków i notatnika
przycisk_gora_rect = przycisk_gora.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 10))
notatnik_rect = notatnik.get_rect(midbottom=(SCREEN_WIDTH // 2, SCREEN_HEIGHT + 200))

# Zmienne sterujące
notatnik_widoczny = False
notatnik_wysuwanie = False

def wysun_notatnik():
    global notatnik_rect
    if notatnik_rect.bottom > SCREEN_HEIGHT - 50:
        notatnik_rect.y -= 30
    else:
        global notatnik_wysuwanie
        notatnik_wysuwanie = False

def opusc_notatnik():
    global notatnik_rect
    if notatnik_rect.bottom < SCREEN_HEIGHT + 200:
        notatnik_rect.y += 10

def toggle_notatnik():
    global notatnik_widoczny, notatnik_wysuwanie
    notatnik_widoczny = not notatnik_widoczny
    if notatnik_widoczny:
        notatnik_wysuwanie = True
    else:
        opusc_notatnik()

# Główna pętla gry
running = True
dzwiek_wywiad.play()

while running:
    screen.blit(tlo1, (0, 0))
    screen.blit(przycisk_gora, przycisk_gora_rect.topleft)

    if notatnik_widoczny:
        screen.blit(notatnik, notatnik_rect.topleft)
        screen.blit(pytanie_text, (450, 120))  # Jeszcze bardziej w prawo

        for i, odp in enumerate(odpowiedzi):
            numer_text = small_font.render(f"{i + 1}. Tak", True, (0, 0, 0))
            nie_text = small_font.render("Nie", True, (0, 0, 0))
            screen.blit(numer_text, (500, 200 + i * 60))  # Jeszcze bardziej w prawo
            screen.blit(nie_text, (630, 200 + i * 60))    # Jeszcze bardziej w prawo

            pygame.draw.rect(screen, (255, 255, 255), odp["tak"])
            pygame.draw.rect(screen, (255, 255, 255), odp["nie"])
            pygame.draw.rect(screen, (0, 0, 0), odp["tak"], 2)
            pygame.draw.rect(screen, (0, 0, 0), odp["nie"], 2)

            if odp["tak_selected"]:
                pygame.draw.line(screen, (0, 0, 0), (odp["tak"].left + 3, odp["tak"].top + 3),
                                 (odp["tak"].right - 3, odp["tak"].bottom - 3), 3)
                pygame.draw.line(screen, (0, 0, 0), (odp["tak"].right - 3, odp["tak"].top + 3),
                                 (odp["tak"].left + 3, odp["tak"].bottom - 3), 3)
            if odp["nie_selected"]:
                pygame.draw.line(screen, (0, 0, 0), (odp["nie"].left + 3, odp["nie"].top + 3),
                                 (odp["nie"].right - 3, odp["nie"].bottom - 3), 3)
                pygame.draw.line(screen, (0, 0, 0), (odp["nie"].right - 3, odp["nie"].top + 3),
                                 (odp["nie"].left + 3, odp["nie"].bottom - 3), 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if przycisk_gora_rect.collidepoint(event.pos):
                toggle_notatnik()
            if notatnik_widoczny:
                for odp in odpowiedzi:
                    if odp["tak"].collidepoint(event.pos):
                        odp["tak_selected"] = True
                        odp["nie_selected"] = False
                    elif odp["nie"].collidepoint(event.pos):
                        odp["nie_selected"] = True
                        odp["tak_selected"] = False

    if notatnik_wysuwanie:
        wysun_notatnik()
    elif not notatnik_widoczny:
        opusc_notatnik()

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
